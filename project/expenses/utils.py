import os
import io
import datetime
from flask import current_app
import xlsxwriter

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
    NOW = str(datetime.datetime.now())
    file_path = os.path.join(DOWNLOADS_PATH, f'{month.user_id}.xlsx')
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    # format variables
    bold = workbook.add_format({'bold': True})
    title = workbook.add_format({'center_across': True, 'bold': True})
    print(f'mjesionc{MONTHS[month.month][1]}')
    # title and headers
    worksheet.write('A1:C1', f'{MONTHS[month.month][0]} {month.year}', title)
    worksheet.write('A2', 'Amount', bold)
    worksheet.write('B2', 'Category', bold)
    worksheet.write('C2', 'Description', bold)

    # body
    row = 2                 # row after headers
    cr_category = ''
    categories_ranges = []  # list of lists with category name and coordinates for sum count
    for expense in month.expenses:
        worksheet.write(row, 0, expense.amount)
        worksheet.write(row, 1, expense.category)
        worksheet.write(row, 2, expense.description)

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
