import xlsxwriter
workbook = xlsxwriter.Workbook('table1.xlsx')
worksheet = workbook.add_worksheet()

row_count = 0
column_count = 0

table_headers = [
    {'header': 'Product'},
    {'header': 'Quarter 1'},
    {'header': 'Quarter 2'},
    {'header': 'Quarter 3'},
    {'header': 'Quarter 4'},
    ]

excel_write_data = [
    ['Apples', 10000, 5000, 8000, 6000],
['Apples', 10000, 5000, 8000, 6000],
['Apples', 10000, 5000, 8000, 6000],
]

table_row_count = row_count + len(excel_write_data)
table_column_count = column_count + len(table_headers)

worksheet.add_table(row_count, column_count,
                    table_row_count, table_column_count,
                    {'data': excel_write_data,
                     'columns': table_headers})

workbook.close()