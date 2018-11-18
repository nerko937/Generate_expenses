import xlsxwriter


def create_xls(expenses):
    workbook = xlsxwriter.Workbook('expenses.xlsx')
    worksheet = workbook.add_worksheet()
    current_record = 1

    for row in expenses:
        worksheet.write(f'A{current_record}', row[4])
        worksheet.write(f'B{current_record}', row[1])
        worksheet.write(f'C{current_record}', row[2])
        worksheet.write(f'D{current_record}', row[3].strftime('%m-%d-%Y'))
        x += 1

    workbook.close()
