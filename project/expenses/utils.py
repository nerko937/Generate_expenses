import os
import io
import datetime
import math

from flask import current_app
import xlsxwriter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
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
    worksheet.set_column(1, 1, 13)
    worksheet.set_column(2, 2, 150)

    # format variables
    bold = workbook.add_format({'bold': True})
    title = workbook.add_format({'bold': 1, 'align': 'center'})
    vcenter = workbook.add_format({'valign': 'vcenter'})
    wrap = workbook.add_format(({'text_wrap': True}))

    # title and headers
    worksheet.merge_range('A1:C1', f'{MONTHS[month.month][1]} {month.year}', title)
    worksheet.write('A2', 'Amount', bold)
    worksheet.write('B2', 'Category', bold)
    worksheet.write('C2', 'Description', bold)

    # body
    row = 2                 # row after headers
    cr_category = ''
    sum_total = 0
    categories_ranges = []  # list of lists with sum, category name and coordinates for excel sum coords
    for expense in month.expenses:
        worksheet.write(row, 0, expense.amount, vcenter)
        worksheet.write(row, 1, expense.category, vcenter)
        worksheet.write(row, 2, expense.description, wrap)

        # categories_ranges appends
        if expense.category != cr_category:
            if len(categories_ranges):
                categories_ranges[-1].append(row - 1)
            cr_category = expense.category
            categories_ranges.append([expense.amount, cr_category, row])
        else:
            categories_ranges[-1][0] += expense.amount
        sum_total += expense.amount
        
        # increment
        row += 1
    
    worksheet.merge_range(f'A{row + 1}:B{row + 1}', 'Summary', title)
    row += 1

    # summary
    if len(categories_ranges):
        categories_ranges[-1].append(row - 1) # finish last coordinate
        categories_ranges.append([sum_total, 'Total', 2, row - 1])
        for sum_cat_data in categories_ranges:
            worksheet.write_formula(                    # sum
                row, 0, f'=SUM(A{sum_cat_data[2] + 1}:A{sum_cat_data[3] + 1}', value=sum_cat_data[0]
            )
            worksheet.write(row, 1, sum_cat_data[1])    # category
            row += 1

    # close
    workbook.close()
    return file_path

def generate_pdf(month):
    '''Generates pdf file in project/downloads directory
    :param month: Month model instance
    :return: path to new file'''
    data = []   # data aka body of pdf
    
    # paragraph styles
    stylesheet = getSampleStyleSheet()
    normal_style = stylesheet['Normal']
    title_style = stylesheet['Heading1']
    title_style.alignment = 1

    title = Paragraph(f'{MONTHS[month.month][1]} {month.year}', title_style)    # title
    data.append(title)

    data.append(Spacer(500, 15))                                                # spacer

    # data for table
    table_data = [
        [
            Paragraph('<b>Amount</b>', normal_style),
            Paragraph('<b>Category</b>', normal_style),                         # headers
            Paragraph('<b>Description</b>', normal_style)
        ],                                                                      # expenses
        *[(exp.amount, exp.category, Paragraph(exp.description, normal_style)) for exp in month.expenses],
    ]

    # styles for table
    styles = TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lavenderblush),
    ])

    # build and append table
    table = Table(table_data, (60, 80, 350))
    table.setStyle(styles)
    data.append(table)

    data.append(Spacer(500, 30))    # spacer

    # preparing summary data
    CAT_NAMES = [el[1] for el in CATEGORIES]
    summary = db.session.query(db.func.sum(Expense.amount)).filter_by(month_id=month.id)
    sums = [
        (summary.filter_by(category=c).first()[0], c) for c in CAT_NAMES
    ]
    sums.append((summary.first()[0], 'Total'))

    # summary table data
    sum_table_data = [
        [Paragraph('<b>Total Amount</b>', normal_style), Paragraph('<b>Category</b>', normal_style)],
        *sums
    ]

    # summary table styles
    sum_styles = TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lavenderblush)
    ])

    # build and append table
    sum_table = Table(sum_table_data)
    sum_table.setStyle(sum_styles)
    data.append(sum_table)

    # build pdf
    file_path = os.path.join(DOWNLOADS_PATH, f'{month.user_id}.pdf')
    doc = SimpleDocTemplate(file_path)
    doc.build(data)
    return file_path
