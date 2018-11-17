import xlsxwriter


def create_xls(expenses):
    workbook = xlsxwriter.Workbook('expenses.xlsx')
    worksheet = workbook.add_worksheet()
    x = 1

    for row in expenses:
        worksheet.write(f'A{x}', row[4])
        worksheet.write(f'B{x}', row[1])
        worksheet.write(f'C{x}', row[2])
        worksheet.write(f'D{x}', row[3].strftime('%m-%d-%Y'))
        x += 1

    workbook.close()
