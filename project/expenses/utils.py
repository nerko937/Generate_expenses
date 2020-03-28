import os
import io
import datetime
import math

from flask import current_app
import xlsxwriter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

from project import db
from .models import Expense


MONTHS = (
	(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
	(5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
	(9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
)

CATEGORIES = (
	('Bills', 'Bills'), ('Entertainment', 'Entertainment'), ('Food', 'Food')
)

DOWNLOADS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'downloads'
)

def generate_xlsx(month):
    '''Generates xlsx file in project/downloads directory
    :param month: Month model instance
    :return: path to new file'''
    # starter
    file_path = os.path.join(DOWNLOADS_PATH, f'{month.user_id}.xlsx')
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()
    worksheet.set_column(1, 2, 13)

    # format variables
    bold = workbook.add_format({'bold': True})
    title = workbook.add_format({'bold': 1, 'align': 'center'})
    vcenter = workbook.add_format({'valign': 'vcenter'})

    # title and headers
    worksheet.merge_range('A1:C1', f'{MONTHS[month.month][0]} {month.year}', title)
    worksheet.write('A2', 'Amount', bold)
    worksheet.write('B2', 'Category', bold)
    worksheet.write('C2', 'Description', bold)

    # body
    row = 2                 # row after headers
    cr_category = ''
    categories_ranges = []  # list of lists with category name and coordinates for sum count
    for expense in month.expenses:
        height = 14
        if len(expense.description) > 150:
            height = math.ceil(len(expense.description) / 150) * 8
            worksheet.set_row(row, height)   # set more row height

        # write row
        worksheet.write(row, 0, expense.amount, vcenter)
        worksheet.write(row, 1, expense.category, vcenter)
        worksheet.insert_textbox(
            row, 2, expense.description, {'width': 1000, 'height': height * 1.3}
        )

        # categories_ranges appends
        if expense.category != cr_category:
            if len(categories_ranges):
                categories_ranges[-1].append(row - 1)
            cr_category = expense.category
            categories_ranges.append([cr_category, row])
        
        # increment
        row += 1

    # summary
    if len(categories_ranges):
        categories_ranges[-1].append(row - 1) # finish last coordinate
        categories_ranges.append(['Total', 2, row - 1])
        # headers
        worksheet.write_row(row, 0, (el[0] for el in categories_ranges), bold)
        # values
        worksheet.write_row(row + 1, 0, (f'=SUM(A{el[1] + 1}:A{el[2] + 1}' for el in categories_ranges))

    # close
    workbook.close()
    return file_path

def generate_pdf(month):
    '''Generates pdf file in project/downloads directory
    :param month: Month model instance
    :return: path to new file'''
    # data aka body of pdf
    data = []
    
    # paragraph styles
    stylesheet = getSampleStyleSheet()
    normal_style = stylesheet['Normal']
    title_style = stylesheet['Heading1']
    title_style.alignment = 1

    # title
    title = Paragraph(f'{MONTHS[month.month][1]} {month.year}', title_style)
    data.append(title)

    # collecting and sorting sums to fit 3-column grid
    sums_headers, sums_values, sums_headers_chunked, sums_values_chunked = [], [], [], []
    UNPACKED_CATEGORIES = [el[1] for el in CATEGORIES]
    summary = db.session.query(db.func.sum(Expense.amount)).filter_by(month_id=month.id)
    for category in UNPACKED_CATEGORIES:
        sums_headers.append(Paragraph(f'<b>{category}</b>', normal_style))
        sums_values.append(summary.filter_by(category=category).first()[0])
    sums_headers.append(Paragraph('<b>Total</b>', normal_style))
    sums_values.append(summary.first()[0])
    for i in range(0, len(sums_headers), 3):
        sums_headers_chunked.append(sums_headers[i:i + 3])
        sums_values_chunked.append(sums_values[i:i + 3])
    sums_sorted = []
    for i in range (len(sums_headers_chunked)):
        sums_sorted.append(sums_headers_chunked[i])
        sums_sorted.append(sums_values_chunked[i])

    # data for table
    table_data = [
        [
            Paragraph('<b>Amount</b>', normal_style),
            Paragraph('<b>Category</b>', normal_style),                             # headers
            Paragraph('<b>Description</b>', normal_style)
        ],
        *[(exp.amount, exp.category, exp.short_descr) for exp in month.expenses],   # expenses
        *sums_sorted                                                                # sums aka. summary
    ]

    # styles for table
    summary_backgrounds = [
        ('BACKGROUND', (0,-i), [-1,-i], colors.lavenderblush)
        for i in range(1, len(sums_sorted) + 1) if i % 2 == 0
    ]
    coord = -3                              # this removes background color from empty headers cells
    last_list_len = len(sums_sorted[-1])
    if last_list_len == 2:
        coord = -2
    if last_list_len == 3:
        coord = -1
    summary_backgrounds[0][2][0] = coord
    styles = TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lavenderblush),
        *summary_backgrounds
    ])

    # build and appen table
    table = Table(table_data)
    table.setStyle(styles)
    data.append(table)

    # build pdf
    file_path = os.path.join(DOWNLOADS_PATH, f'{month.user_id}.pdf')
    doc = SimpleDocTemplate(file_path)
    doc.build(data)
    return file_path

def get_file(file_path):
    '''Puts file in memory, removes the one provided by path, returns the memory one
    file_path: string
    :return: file for download'''
    return_data = io.BytesIO()
    with open(file_path, 'rb') as fo:
        return_data.write(fo.read())
    return_data.seek(0)

    os.remove(file_path)

    return return_data
