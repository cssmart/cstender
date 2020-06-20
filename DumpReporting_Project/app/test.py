import xlsxwriter

workbook = xlsxwriter.Workbook('tables_data.xlsx')
worksheet1 = workbook.add_worksheet()
row_count = 15
column_count = 1
caption = 'Passbook'
bold = workbook.add_format({'bold': True})
format = workbook.add_format()
format.set_font_size(30)
worksheet1.insert_image('G1', 'app/static/logo.jpg', {'x_scale': 0.5, 'y_scale': 0.5})
worksheet1.write('D5', 'Customer Ledger Passbook', format)

# Some sample data for the table.
data = [
    ['Organization Id', 10000],
    ['Organization', 2000,],
    ['Customer Name', 6000],
    ['Customer Site Address', 500],
    ['Customer Number', 500],
    ['Date From', 500],
    ['Date To', 500],
    ['Customer TYPE', 500],

]
opening_bal = [
    ['Organization Id', 10000,999],


]
# Write the caption.
worksheet1.write('B1', caption, bold)

# Add a table to the worksheet.
worksheet1.add_table('B2:C9',{'data': data})
worksheet1.add_table('E13:G14',{'data': opening_bal,
                                'columns': [{'header': 'Opening Balance'},
                                           {'header': 'OP_TOT_DR'},
                                           {'header': 'OP_TOT_CR'},
                                           ]})

worksheet1.write('B11', 'RUNTOT', bold)
# worksheet1.write('E13', 'Opening Balance', bold)
# worksheet1.write('F13', 'OP_TOT_DR', bold)
# worksheet1.write('G13', 'OP_TOT_CR', bold)

running_bal = [
[168916.96]
    ,[ 236413.94],[ 156997.58],[ 66536.18], [54877.17999999999]
]
#
excel_write_data = [
    ['Apples', 10000, 5000, 8000, 6000,33],
['Apples', 10000, 5000, 8000, 6000,33],
['Apples', 10000, 5000, 8000, 6000,33],
    ['Apples', 10000, 5000, 8000, 6000,33],
['Apples', 10000, 5000, 8000, 6000,33],
]
opening =151475.18
for i in excel_write_data:
    print(i[4],'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    da =  opening + i[4] - i[5]
    print(da,'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')

table_row_count = row_count + len(excel_write_data)
print(table_row_count,'wwwwwww')
col_count = 8
worksheet1.add_table(row_count, col_count,
                     table_row_count, 8,
                     {'data': running_bal,
                                'columns': [{'header': 'Running Balance'},
                                           ]})

table_headers =worksheet1.add_table(row_count, column_count,
                    table_row_count, 7,{'data':excel_write_data,
                               'columns': [{'header': 'Document No.'},
                                           {'header': 'Document Date'},
                                           {'header': 'Document Type'},
                                           {'header': 'Reference'},
                                           {'header': 'Debit'},
                                           {'header': 'Credit'},
                                           {'header': 'Remarks'},

                                           ]})

row1_count =table_row_count +3
table_row_count_1 = row1_count+2
print(table_row_count_1,'xxxxxxxxxxxx')

data_below = [
    ['Organization Id',11,11],
]
column_count_ =6
worksheet1.add_table(row1_count, column_count_,
                     table_row_count_1,6,{'data':data_below,
                               'columns': [{'header': 'Closing Balance'},
                                           ]})
workbook.close()