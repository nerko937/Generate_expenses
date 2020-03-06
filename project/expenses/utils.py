import os
from flask import current_app
import xlsxwriter

DOWNLOADS_PATH = os.path.join(app.instance_path, 'project', 'downloads')

def generate_xlsx(month):
    file_path = os.path.join(DOWNLOADS_PATH, f'{month.year}-{month.month}_{month.user_id}')
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()
    current_record = 1

    for row in expenses:
        worksheet.write(f'A{current_record}', row[4])
        worksheet.write(f'B{current_record}', row[1])
        worksheet.write(f'C{current_record}', row[2])
        worksheet.write(f'D{current_record}', row[3].strftime('%m-%d-%Y'))
        x += 1

    workbook.close()