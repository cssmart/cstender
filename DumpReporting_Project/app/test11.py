import xlsxwriter

workbook  = xlsxwriter.Workbook('file.xlsx')
worksheet = workbook.add_worksheet()

data = [13, 24, 15]
for row_num, value in enumerate(data):
    row_num += 1

    worksheet.write(row_num, 0, value)


    worksheet.write(row_num, 10, '=SUM(A1:A{})'.format(row_num))

workbook.close()