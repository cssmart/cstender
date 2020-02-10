from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import xlsxwriter
import cx_Oracle
from io import BytesIO, StringIO
from .forms import DumpForm
from .models import DUMPReport
from django.http import HttpResponse
from rest_framework.decorators import api_view
import psycopg2


def dump_report_view(request):
    # if request.method == 'POST':
    form = DumpForm(request.POST or None)
    print(form, 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    print(request.method, '2111111111111111')
    print(form.is_valid(), 'qqqqqqqqqq222222222222222222222222222222222222222')
    if form.is_valid():
        data = form.save(commit=False)
        business_line = form.cleaned_data['business_line']
        business_unit = form.cleaned_data['business_unit']
        shipping_org = form.cleaned_data['shipping_org']
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']
        unit = form.cleaned_data['unit']
        sales_account = form.cleaned_data['sales_account']
        # data_save = DUMPReport(business_line=business_line, business_unit=business_unit, shipping_org=shipping_org,
        #                        from_date=from_date, to_date=to_date, unit=unit, sales_account=sales_account)
        # data_save.save()
        form.save()
        # return HttpResponseRedirect('')
        return redirect('')
    else:
        print(form.errors)
    # context ={
    #     'form':form
    # }
    return render(request, 'app/app/dump_report_create.html', {'form':form})


@api_view(['POST'])
def dump_report_data(request):
    data = request.data
    business_unit = data['business_unit']
    business_line_input = data['business_line']
    from_date = data['from_date']
    to_date = data['to_date']
    unit = data['unit']
    sales_account = data['sales_account']
    dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
    output = BytesIO()
    conn = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns)
    print(conn)
    cursor = conn.cursor()
    print(cursor)
    data = f"""
    select V.EXCHANGE_RATE,
    V.BUSINESS_UNIT,
    V.BUSINESS_LINE,
    V.EVENT_CLASS_CODE,
    V.ENTITY_CODE,
    V.DEL_ORG_ID,
    MIN(V.DELIVERY_DETAIL_ID) DELIVERY_DETAIL_ID,
    V.CONSIGNEE_NAME,
    V.BILL_TO_SITE_USE_ID,
    V.SHIP_TO_SITE_USE_ID,
    V.RAC_BILL_TO_CUSTOMER_NAME,
    V.CUST_ID,
    V.RAA_BILL_TO_CONCAT_ADDRESS,
    V.RAA_BILL_TO_POSTAL_CODE,
    V.RAA_BILL_TO_STATE,
    V.ORDERED_DATE,
    MIN(V.SHIP_TIME) SHIP_TIME,
    V.TRX_DATE,
    V.TERMS,
    V.CUST_PO_NUMBER,
    V.PROJ,
    V.CUSTPODATE,
    V.DELIVERY_ID,
    V.OA_NO,
    V.ORDER_TYPE,
    V.CUR,
    sum(V.NET) NET,
    V.GROSS,
    V.GROSS_WEIGHT,
    V.HEADER_ID,
    V.SP_INS,
    V.VOLUME,
    V.RAT_TERM_NAME,
    V.FOB,
    max(V.GST_DATE) GST_DATE,
    max(V.GST_TIME) GST_TIME,
    nvl(v1.INVENTORY_ITEM_ID,V.INVENTORY_ITEM_ID) INVENTORY_ITEM_ID,
    NVL(V1.ITEM_CODE,V.ITEM_CODE) ITEM_CODE,
    NVL(V1.DESCRIPTION,V.DESCRIPTION) DESCRIPTION,
    NVL(V1.UNIT_CODE,V.UNIT_CODE) UNIT_CODE,
    MIN(V.LINE_NUMBER) LINE_NUMBER,
    SUM(NVL(V1.QUANTITY,V.QUANTITY)) QUANTITY,
    NVL(V1.UNIT_SELLING_PRICE,V.UNIT_PRICE) UNIT_PRICE ,
    V.CONVERSION_RATE,
    V.WAYBILL,
    V.TRX_NUMBER,
    SUM(V.REVENUE_AMOUNT) REVENUE_AMOUNT,
    V.REV_UNIT,
    V.REV_ACCOUNT,
    V.REV_ACCT_DESC,
    V.SHIPPING_ORG,
    V.CUSTOMER_NUMBER,
    V.SHIP_CUSTOMER,
    V.SHIP_CUST_GSTN,
    V.SHIP_CUST_STATE,
    V.CUSTOMER_CLASS_CODE,
    V.CUSTOMER_CATEGORY_CODE,
    V.DOM_IBD,
    V.ZONE,
    V.REGION,
    V.BRANCH,
    V.COUNTRY,
    V.SALESREP_ID,
    V.COMM,
    V.TRX_CLASS,
    SUM(V.TAXABLE_VALUE) TAXABLE_VALUE,
    V.TAX_INVOICE_NUM,
    V.RETURN_REASON_CODE,
    V.RETURN_ORDER_NUM,
    V.RETURN_INVOICE_NUM,
    max(V.TAX_INVOICE_DATE) TAX_INVOICE_DATE,
    V.TRX_ID,
    MIN(V.TRX_LINE_ID) TRX_LINE_ID,
    V.ORG_ID,
    V.SUPPLIER_GST_NUMBER,
    V.SUPPLIER_PAN_NUM,
    V.CUSTOMER_GST_NUM,
    V.CUSTOMER_PAN_NUM,
    SUM(V.CGST) CGST,
    V.CGST_RATE,
    SUM(V.SGST) SGST,
    V.SGST_RATE,
    SUM(V.IGST) IGST,
    V.IGST_RATE,
    V.CURRENCY_CONVERSION_RATE,
    V.REGIME_CODE,
    V.GST_EVENT_CLASS_CODE,
    V.GST_ENTITY_CODE,
    MIN(V.DET_FACTOR_ID) DET_FACTOR_ID,
    V.SUPP_STATE,
    V.BILL_STATE,
    SUM(V.FREIGHT) FREIGHT,
    SUM(V.INSURANCE) INSURANCE,
    SUM(V.PACKING) PACKING,
    SUM(V.TCS) TCS,
    V.SALES_PERSON,
    V.ORDER_CLASS,
    V.MIS_CAT1,
    V.MIS_CAT2,
    V.HSN_SAC,
    V.ADDRESSEE,
    V.TAX_CATEGORY_NAME,
    V.CREDIT_MEMO_NUM,
    V.CREDIT_MEMO_DATE
    from apps.XXCNS_SALES_RETURN V,
            CNSTECH2.XXCNS_BTBD_ITEM_DETAILS V1
    where V.CUSTOMER_TRX_ID=V1.CUSTOMER_TRX_ID(+)
    AND V.CUSTOMER_TRX_LINE_ID=V1.CUSTOMER_TRX_LINE_ID(+)
    AND trunc(V.trx_date) between '{from_date}' and '{to_date}' and rownum<=10
    and V.business_line = NVL('{business_line_input}',business_line)
    and V.business_unit = NVL('{business_unit}',business_unit)
    and nvl(substr(v.rev_account,1,4),'X') = nvl('{unit}',nvl(substr(v.rev_account,1,4),'X'))
    and nvl(substr(rev_account,6,7),'X') = nvl('{sales_account}',nvl(substr(rev_account,6,7),'X'))
    GROUP BY V.EXCHANGE_RATE,
    V.BUSINESS_UNIT,
    V.BUSINESS_LINE,
    V.EVENT_CLASS_CODE,
    V.ENTITY_CODE,
    V.DEL_ORG_ID,
    V.CONSIGNEE_NAME,
    V.BILL_TO_SITE_USE_ID,
    V.SHIP_TO_SITE_USE_ID,
    V.RAC_BILL_TO_CUSTOMER_NAME,
    V.CUST_ID,
    V.RAA_BILL_TO_CONCAT_ADDRESS,
    V.RAA_BILL_TO_POSTAL_CODE,
    V.RAA_BILL_TO_STATE,
    V.ORDERED_DATE,
    V.TRX_DATE,
    V.TERMS,
    V.CUST_PO_NUMBER,
    V.PROJ,
    V.CUSTPODATE,
    V.DELIVERY_ID,
    V.OA_NO,
    V.ORDER_TYPE,
    V.CUR,
    V.GROSS,
    V.GROSS_WEIGHT,
    V.HEADER_ID,
    V.SP_INS,
    V.VOLUME,
    V.RAT_TERM_NAME,
    V.FOB,
    V.GST_DATE,
    V.GST_TIME,
    nvl(v1.INVENTORY_ITEM_ID,V.INVENTORY_ITEM_ID),
    NVL(V1.ITEM_CODE,V.ITEM_CODE),
    NVL(V1.DESCRIPTION,V.DESCRIPTION),
    NVL(V1.UNIT_CODE,V.UNIT_CODE),
    NVL(V1.UNIT_SELLING_PRICE,V.UNIT_PRICE),
    V.CONVERSION_RATE,
    V.WAYBILL,
    V.TRX_NUMBER,
    V.REV_UNIT,
    V.REV_ACCOUNT,
    V.REV_ACCT_DESC,
    V.SHIPPING_ORG,
    V.CUSTOMER_NUMBER,
    V.SHIP_CUSTOMER,
    V.SHIP_CUST_GSTN,
    V.SHIP_CUST_STATE,
    V.CUSTOMER_CLASS_CODE,
    V.CUSTOMER_CATEGORY_CODE,
    V.DOM_IBD,
    V.ZONE,
    V.REGION,
    V.BRANCH,
    V.COUNTRY,
    V.SALESREP_ID,
    V.COMM,
    V.TRX_CLASS,
    V.TAX_INVOICE_NUM,
    V.RETURN_REASON_CODE,
    V.RETURN_ORDER_NUM,
    V.RETURN_INVOICE_NUM,
    V.TRX_ID,
    V.ORG_ID,
    V.SUPPLIER_GST_NUMBER,
    V.SUPPLIER_PAN_NUM,
    V.CUSTOMER_GST_NUM,
    V.CUSTOMER_PAN_NUM,
    V.CGST_RATE,
    V.SGST_RATE,
    V.IGST_RATE,
    V.CURRENCY_CONVERSION_RATE,
    V.REGIME_CODE,
    V.GST_EVENT_CLASS_CODE,
    V.GST_ENTITY_CODE,
    V.SUPP_STATE,
    V.BILL_STATE,
    V.SALES_PERSON,
    V.ORDER_CLASS,
    V.MIS_CAT1,
    V.MIS_CAT2,
    V.HSN_SAC,
    V.ADDRESSEE,
    V.TAX_CATEGORY_NAME,
    V.CREDIT_MEMO_NUM,
    V.CREDIT_MEMO_DATE"""
    cur = cursor.execute(data)
    print(cur)
    data_list = []
    for i in cur:
        data = i
        data_list.append(i)
    data_list =data_list
    res = str(data_list)[1:-1]
    # try:
    #     connection = psycopg2.connect(user="dump_user", password="password", host="127.0.0.1", port="5433",
    #                                   database="dump_report_db")
    #     TABLE_NAME = "dump_report"
    #     cursor = connection.cursor()
    #     # sql_statement = "DROP TABLE dump_report_table ;"
    #     sql_statement = """
    #     CREATE TABLE {} (EXCHANGE_RATE VARCHAR(32),
    #     BUSINESS_UNIT VARCHAR(64),
    #     BUSINESS_LINE VARCHAR(32),
    #     EVENT_CLASS_CODE VARCHAR(32));""".format(TABLE_NAME)
    #     print(sql_statement)
    #     cursor.execute(sql_statement)
    #     connection.commit()
    #     print("Table created successfully in PostgreSQL ")
    #     sql_stat = f"""INSERT INTO dump_report (EXCHANGE_RATE, BUSINESS_UNIT,BUSINESS_LINE,EVENT_CLASS_CODE)
    #     VALUES {res};"""
    #     cursor.execute(sql_stat)
    #     connection.commit()
    #     print("Data inserted successfully in Table !!")
    # except (Exception, psycopg2.DatabaseError) as error:
    #     print("Error while creating PostgreSQL table", error)
    context = {
        "data_list": data_list
    }
    return render(request, 'app/app/dump_report.html', context)