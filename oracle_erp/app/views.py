from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import xlsxwriter
import cx_Oracle
from io import BytesIO
from .forms import ERPForm
from .models import ERPReport
from django.http import HttpResponse


def sales_return_report(request):
    '''
    Create Sales Return Report
    :param request:
    :return:
    '''
    dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
    output = BytesIO()
    conn = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns)
    # cx_Oracle.connect is used to connect the  oracle database
    data = """
    select V.EXCHANGE_RATE,V.BUSINESS_UNIT,
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
    AND trunc(V.trx_date) between '01-APR-19' and '30-APR-19'
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
    cursor = conn.cursor()
    acess_data_query = cursor.execute(data)
    list_data = []
    for acess_data in acess_data_query:
        list_data.append(acess_data)
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    col = 0
    for row, data in enumerate(list_data):
        worksheet.write_row(row, col, data)
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return response


def erp_view(request):
    if request.method == 'POST':
        form = ERPForm(request.POST)
        if form.is_valid():
            business_line = form.cleaned_data['business_line']
            business_unit = form.cleaned_data['business_unit']
            shipping_org = form.cleaned_data['shipping_org']
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            unit = form.cleaned_data['unit']
            sales_account = form.cleaned_data['sales_account']
            # data_save = ERPReport(business_line=business_line, business_unit=business_unit, shipping_org=shipping_org,
            #                       from_date=from_date, to_date=to_date, unit=unit, sales_account=sales_account)
            # data_save.save()
            form.save()
        return HttpResponseRedirect('app:sales', request)
    else:
        form = ERPForm()
    return render(request, 'app/app/erp_template.html', {'form': form})
