from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import xlsxwriter
import cx_Oracle
from io import BytesIO, StringIO
from app.forms import ContributionReportForm,ContributionReportDownload
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import psycopg2
from django.contrib import messages
TABLE_REPORT_NAME = "public.dump_table_report"
from django.db import connection
from datetime import datetime
from app.db import oracle_db_connection
import pandas as pd


TABLE_NAME='contribution_report_27feb2'
REPLACE_TABLE_NAME='contribution_report_data6'

table_create =f""" CREATE TABLE {TABLE_NAME} (org_id VARCHAR(300),
shipping_org VARCHAR(300),
inv_org VARCHAR(300),
region VARCHAR(300),
sub_region VARCHAR(300),
branch VARCHAR(300),
customer_code VARCHAR(300),
customer_name VARCHAR(300),
customer_class_code VARCHAR(300),
customer_category_code VARCHAR(300),
cusomer_clasification VARCHAR(300),
sales_order_no VARCHAR(300),
sales_order_type VARCHAR(300),
order_category VARCHAR(300),
sales_persion VARCHAR(300),
trx_class VARCHAR(300),
dom_ibd VARCHAR(300),
transaction_type VARCHAR(300),
transaction_number VARCHAR(300),
trx_date VARCHAR(300),
invoice_currency_code VARCHAR(300),
REFERENCE VARCHAR(300),
mis_cat1 VARCHAR(300),
mis_cat2 VARCHAR(300),
item_type1 VARCHAR(300),
item_type2 VARCHAR(300),
item_type3 VARCHAR(300),
item_type4 VARCHAR(300),
item_name VARCHAR(300),
item_description VARCHAR(300),
quantity_invoiced VARCHAR(300),
revenue_unit VARCHAR(300),
revenue_account VARCHAR(300),
revenue_acct_desc VARCHAR(300),
sale_amount VARCHAR(300),
excise_amount VARCHAR(300),
stvat VARCHAR(300),
inclusive_tax VARCHAR(300),
net_sales VARCHAR(300),
cogs_unit VARCHAR(300),
cogs_account VARCHAR(300),
cogs_acct_desc VARCHAR(300),   
cogs_quantity VARCHAR(300),   
material_cost VARCHAR(300),
osp_cost VARCHAR(300), 
resource_cost VARCHAR(300),
cogs_amount VARCHAR(300),
transaction_id VARCHAR(300),
project_number VARCHAR(300),
project_name VARCHAR(300),
GST_INVOICE_NUMBER VARCHAR(300),
lp VARCHAR(300),
spcl_inst  VARCHAR(300)
)"""

def contribution_report_parameter(request):
    '''
    Create front view to access the data from the oracle DB..
    :param request:
    :return:
    '''
    form = ContributionReportForm(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        form.save()
        return redirect('.')
    else:
        print(form.errors)
    return render(request, 'app/app/contribution_report_form.html', {'form': form})


@api_view(['POST'])
def contribution_get_report_data(request):
    data = request.data
    ladger_id = data['ladger_id']
    table_type = data['table_type']
    unit = data['unit']
    from_date = data['from_date']
    to_date = data['to_date']
    print(data,'ddddddddddddddddddddd', to_date)

    dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
    conn_ora = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns)
    cursor_ora = conn_ora.cursor()
    list_data = f""" select   org_id, shipping_org, inv_org,  region,  sub_region,  branch,
               customer_code,  customer_name, customer_class_code, customer_category_code, cusomer_clasification,  sales_order_no,
                sales_order_type,   order_category, sales_persion, trx_class,   dom_ibd,
               transaction_type,   transaction_number,   trx_date,
                invoice_currency_code, REFERENCE,  mis_cat1,  mis_cat2,  item_type1,
               item_type2,  item_type3,  item_type4,  item_name, TRANSLATE(item_description,'<>',' ') item_description,
               (case when instr(upper(sales_order_type), 'RETURN') > 0 then quantity_invoiced*-1 else quantity_invoiced end) quantity_invoiced,  revenue_unit,  revenue_account,  revenue_acct_desc,
                sale_amount,   excise_amount,  stvat,  inclusive_tax,
                 net_sales,  cogs_unit, cogs_account,
                cogs_acct_desc,   
    			(case when instr(upper(sales_order_type), 'RETURN') > 0 then cogs_quantity*-1 else cogs_quantity end) cogs_quantity,   
    			material_cost,   osp_cost,
               resource_cost,   cogs_amount,   transaction_id,  project_number,apps.XXCNS_CNTBN_REPORT_PKG.GET_Project_Name(project_number) project_name,  GST_INVOICE_NUMBER, lp, TRANSLATE(spcl_inst,'<>',' ') spcl_inst 
    from (
        (
        (SELECT   MAX(org_id) org_id, MAX(shipping_org) shipping_org, MAX(inv_org) inv_org, MAX(region) region, MAX(sub_region) sub_region, MAX(branch) branch,
                  MAX(customer_code) customer_code, MAX(customer_name) customer_name, MAX(customer_class_code) customer_class_code, MAX(customer_category_code) customer_category_code,
        		  MAX(cusomer_clasification) cusomer_clasification, MAX(sales_order_no) sales_order_no,
                   MAX(sales_order_type) sales_order_type,  MAX(order_category) order_category, MAX(sales_persion) sales_persion,  MAX(trx_class) trx_class,  MAX(dom_ibd) dom_ibd,
                   MAX(transaction_type) transaction_type,  MAX(transaction_number) transaction_number,  MAX(trx_date) trx_date,
                   MAX(invoice_currency_code) invoice_currency_code,  MAX(REFERENCE) REFERENCE,  MAX(mis_cat1) mis_cat1,  MAX(mis_cat2) mis_cat2,  MAX(item_type1) item_type1,
                   MAX(item_type2) item_type2,  MAX(item_type3) item_type3,  MAX(item_type4) item_type4, MAX(item_name) item_name, MAX(item_description) item_description,
                   MIN(quantity_invoiced) quantity_invoiced,  MAX(revenue_unit) revenue_unit, MAX(revenue_account) revenue_account, MAX(revenue_acct_desc) revenue_acct_desc,
                   SUM(sale_amount) sale_amount,  SUM(excise_amount) excise_amount,  SUM(stvat) stvat,  SUM(inclusive_tax) inclusive_tax,
                   SUM(net_sales)  net_sales,  MAX(cogs_unit) cogs_unit,  MAX(cogs_account) cogs_account,
                   MAX(cogs_acct_desc) cogs_acct_desc,  MAX(cogs_quantity) cogs_quantity, MAX(material_cost)  material_cost,  MAX(osp_cost) osp_cost,
                   SUM(resource_cost) resource_cost,  SUM(cogs_amount) cogs_amount,   transaction_id,  MAX(project_number) project_number, max(Inv_Num) GST_INVOICE_NUMBER,
        		   sum(lp) lp, max(spcl_inst) spcl_inst
        FROM           
        (        
        --Query for COGS calculation (With TRANSACTION_ID)--
           select     YY.ORG_ID
            ,   (select hou.NAME from HR_OPERATING_UNITS HOU where HOU.ORGANIZATION_ID=YY.ORG_ID) SHIPPING_ORG
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_organization_name(MMT.ORGANIZATION_ID) INV_ORG
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_region(NVL(XX.territory_id,YY.territory_id)) REGION
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_sub_region(NVL(XX.territory_id,YY.territory_id)) SUB_REGION
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_branch(NVL(XX.territory_id,YY.territory_id)) BRANCH
            ,   YY.CUSTOMER_NUMBER  CUSTOMER_CODE
            ,   YY.CUSTOMER_NAME
        	,   YY.CUSTOMER_CLASS_CODE
        	,   (SELECT hca_bill.customer_category_code 
        		FROM   hz_cust_site_uses_all hcs_bill, 
        			   hz_cust_acct_sites_all hca_bill 
        		WHERE  hcs_bill.site_use_id = XX.bill_to_site_use_id
        			   AND hcs_bill.site_use_code = 'BILL_TO' 
        			   AND hca_bill.cust_acct_site_id = hcs_bill.cust_acct_site_id ) customer_category_code
            ,   YY.attribute6 cusomer_clasification 
            ,   to_char(yy.order_number) SALES_ORDER_NO
            ,   (select ot.name from  oe_transaction_types_tl ot where ot.transaction_type_id = yy.order_type_id AND ot.LANGUAGE = USERENV ('LANG')) SALES_ORDER_TYPE
            ,   yy.ATTRIBUTE5  ORDER_CATEGORY
            ,   apps.arpt_sql_func_util.get_salesrep_name_number (XX.primary_salesrep_id,'NAME') sales_persion
                ,(select rctta.TYPE from RA_CUST_TRX_TYPES_ALL RCTTA where RCTTA.CUST_TRX_TYPE_ID = XX.CUST_TRX_TYPE_ID and RCTTA.ORG_ID = XX.ORG_ID) TRX_CLASS
                ,apps.XXCNS_CNTBN_REPORT_PKG.get_dom_ibd(NVL(XX.territory_id,YY.territory_id)) DOM_IBD 
               -- ,(select rctta.DESCRIPTION from RA_CUST_TRX_TYPES_ALL RCTTA where RCTTA.CUST_TRX_TYPE_ID = XX.CUST_TRX_TYPE_ID and RCTTA.ORG_ID = XX.ORG_ID) TRANSACTION_TYPE
               ,NVL((select rctta.DESCRIPTION from RA_CUST_TRX_TYPES_ALL RCTTA where RCTTA.CUST_TRX_TYPE_ID = XX.CUST_TRX_TYPE_ID and RCTTA.ORG_ID = XX.ORG_ID),
               (select mtt.transaction_type_name FROM mtl_transaction_types mtt where mtt.transaction_type_id = mmt.transaction_type_id)) TRANSACTION_TYPE
                ,XX.TRX_NUMBER TRANSACTION_NUMBER
                ,TO_CHAR(XX.TRX_DATE,'DD-MON-RRRR') TRX_DATE
                ,XX.invoice_currency_code
                ,XX.CT_REFERENCE REFERENCE
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_mis_cat(MMT.INVENTORY_ITEM_ID,MMT.ORGANIZATION_ID,1) MIS_CAT1
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_mis_cat(MMT.INVENTORY_ITEM_ID,MMT.ORGANIZATION_ID,2) MIS_CAT2
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_item_type1(MMT.INVENTORY_ITEM_ID,MMT.ORGANIZATION_ID) ITEM_TYPE1
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_item_type2(MMT.INVENTORY_ITEM_ID,MMT.ORGANIZATION_ID) ITEM_TYPE2
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_item_type3(MMT.INVENTORY_ITEM_ID,MMT.ORGANIZATION_ID) ITEM_TYPE3
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_item_type4(MMT.INVENTORY_ITEM_ID,MMT.ORGANIZATION_ID) ITEM_TYPE4  
                ,(select MSI.SEGMENT1 from MTL_SYSTEM_ITEMS_B MSI where MSI.INVENTORY_ITEM_ID = MMT.INVENTORY_ITEM_ID and MSI.ORGANIZATION_ID = MMT.ORGANIZATION_ID) ITEM_NAME
                ,YY.DESCRIPTION  ITEM_DESCRIPTION
                ,ABS(MMT.TRANSACTION_QUANTITY) QUANTITY_INVOICED
                ,NULL   REVENUE_UNIT
                ,NULL REVENUE_ACCOUNT
                ,NULL REVENUE_ACCT_DESC
                ,NULL SALE_AMOUNT
                ,NULL EXCISE_AMOUNT
                ,NULL STVAT
                ,NULL INCLUSIVE_TAX
                ,NULL NET_SALES
                ,GCC.SEGMENT1 COGS_UNIT
                ,GCC.SEGMENT1||'.'||GCC.SEGMENT2||'.'||GCC.SEGMENT3||'.'||GCC.SEGMENT4||'.'||GCC.SEGMENT5 COGS_ACCOUNT
                ,apps.XXCNS_CNTBN_REPORT_PKG.get_segment2_desc(GCC.SEGMENT2) COGS_ACCT_DESC
                --,ABS(MMT.TRANSACTION_QUANTITY) COGS_QUANTITY
        		,ABS(case when MMT.TRANSACTION_TYPE_ID = 10008 and MMT.TRANSACTION_ACTION_ID = 36 and MMT.TRANSACTION_SOURCE_TYPE_ID = 2 and MMT.TRANSACTION_SOURCE_NAME is NOT NULL
                  then (select MMT1.TRANSACTION_QUANTITY 
                       from mtl_material_transactions mmt1 
                       where mmt1.transaction_id = (select max(MMT2.TRANSACTION_ID)
                                              from mtl_material_transactions MMT2
                                              where mmt2.TRANSACTION_TYPE_ID = 33 
                                              and mmt2.TRANSACTION_ACTION_ID = 1 
                                              and mmt2.TRANSACTION_SOURCE_TYPE_ID = 2 
                                              and mmt2.TRANSACTION_SOURCE_NAME is NULL
                                              and mmt2.TRANSACTION_SOURCE_ID = mmt.TRANSACTION_SOURCE_ID
                                              and mmt2.TRX_SOURCE_LINE_ID = mmt.TRX_SOURCE_LINE_ID))
                 else  mmt.TRANSACTION_QUANTITY
                 end)  COGS_QUANTITY
                ,apps.XXCNS_CNTBN_REPORT_PKG.GET_MATERIAL_COST(MMT.TRANSACTION_ID) MATERIAL_COST
                ,apps.XXCNS_CNTBN_REPORT_PKG.GET_OSP_COST(MMT.TRANSACTION_ID) OSP_COST
                ,apps.XXCNS_CNTBN_REPORT_PKG.GET_RESOURCE_COST(MMT.TRANSACTION_ID) RESOURCE_COST
                ,(NVL (xel.accounted_dr, 0) - NVL (xel.accounted_cr, 0)) COGS_AMOUNT
                --,MMT.TRANSACTION_ID
                ,(case when MMT.TRANSACTION_TYPE_ID = 10008 and MMT.TRANSACTION_ACTION_ID = 36 and MMT.TRANSACTION_SOURCE_TYPE_ID = 2 and MMT.TRANSACTION_SOURCE_NAME is NOT NULL
                 then (select max(MMT2.TRANSACTION_ID)
                       from mtl_material_transactions MMT2
                       where mmt2.TRANSACTION_TYPE_ID = 33 and mmt2.TRANSACTION_ACTION_ID = 1 and mmt2.TRANSACTION_SOURCE_TYPE_ID = 2 and mmt2.TRANSACTION_SOURCE_NAME is NULL
                       and mmt2.TRANSACTION_SOURCE_ID = mmt.TRANSACTION_SOURCE_ID
                       and mmt2.TRX_SOURCE_LINE_ID = mmt.TRX_SOURCE_LINE_ID)
                 else  mmt.transaction_id
                 end) TRANSACTION_ID
                ,xx.attribute2 PROJECT_NUMBER 
                ,(select max(TAX_INVOICE_NUM)       
                FROM   apps.jai_tax_lines_v jtl 
                WHERE  jtl.entity_code LIKE 'TRANSACTIONS'
                AND jtl.APPLICATION_ID = 222
                AND  jtl.TRX_ID = xx.CUSTOMER_TRX_ID
                AND jtl.trx_line_id = xx.CUSTOMER_TRX_LINE_ID 
                AND jtl.TAX_RATE_TYPE  NOT LIKE '%ADHOC%') Inv_Num, yy.lp,  yy.spcl_inst
            FROM apps.xla_transaction_entities_upg xte,
                 apps.xla_events xe,
                 apps.xla_ae_headers xeh,
                 apps.xla_ae_lines xel,
                 gl_code_combinations gcc,
                 (select ooha.order_number, ooha.header_id, ooha.order_type_id, OOHA.ATTRIBUTE5, OOLA.ORG_ID, oola.LINE_ID, msi.DESCRIPTION, ARC.CUSTOMER_NUMBER, ARC.CUSTOMER_NAME, ARC.attribute6, ARC.CUSTOMER_CLASS_CODE
                 ,(SELECT terr.territory_id FROM hz_cust_site_uses_all ship_su, ra_territories terr WHERE  ship_su.site_use_id = oola.invoice_to_org_id AND ship_su.territory_id = terr.territory_id) territory_id
        		 ,(oola.unit_list_price * oola.ordered_quantity) lp, SUBSTR (ooha.attribute20, 1, 45) spcl_inst
        		 from oe_order_headers_all ooha,
                 oe_order_lines_all oola,
                 MTL_SYSTEM_ITEMS_B                  MSI,
                 AR_CUSTOMERS                        ARC
                 where 1 = 1
                 AND ooha.HEADER_ID=oola.HEADER_ID
                 and ARC.CUSTOMER_ID = ooha.sold_to_org_id        
                 AND oola.SHIP_FROM_ORG_ID       =   MSI.ORGANIZATION_ID
                 AND oola.INVENTORY_ITEM_ID      =   MSI.INVENTORY_ITEM_ID 
                 ) yy,
                 (select RCTA.attribute2, rcta.CT_REFERENCE, rcta.invoice_currency_code,
                         RCTA.TRX_DATE,RCTA.TRX_NUMBER,RCTA.territory_id,rcta.primary_salesrep_id, rcta.INTERFACE_HEADER_ATTRIBUTE1, rcta.INTERFACE_HEADER_ATTRIBUTE2, 
                         RCTA.CUST_TRX_TYPE_ID, RCTA.BILL_TO_SITE_USE_ID,
                         RCTLA.SALES_ORDER, RCTLA.ORG_ID, RCTLA.SALES_ORDER_LINE, RCTLA.INTERFACE_LINE_ATTRIBUTE6,
                         RCTLA.DESCRIPTION, RCTLA.customer_trx_id, RCTLA.customer_trx_line_id, RCTLA.QUANTITY_INVOICED,RCTLA.QUANTITY_CREDITED, RCTLA.UNIT_SELLING_PRICE,
                         OHA.HEADER_ID, OLA.LINE_ID               
                 from OE_ORDER_HEADERS_ALL                 OHA,
                      OE_ORDER_LINES_ALL                  OLA,
                      RA_CUSTOMER_TRX_LINES_ALL           RCTLA,
                      RA_CUSTOMER_TRX_ALL                 RCTA 
                 WHERE 1 = 1
                 AND RCTA.CUSTOMER_TRX_ID            =  RCTLA.CUSTOMER_TRX_ID
                 AND RCTA.ORG_ID                     =  RCTLA.ORG_ID 
                 AND RCTLA.SALES_ORDER               =   OHA.ORDER_NUMBER
                 AND RCTLA.ORG_ID                    =   OHA.SOLD_FROM_ORG_ID
                 AND RCTLA.SALES_ORDER_LINE          =   OLA.LINE_NUMBER
                 AND RCTLA.INTERFACE_LINE_ATTRIBUTE6 =   to_char(OLA.LINE_ID)
                 AND RCTLA.INTERFACE_LINE_CONTEXT    = 'ORDER ENTRY'
                 AND RCTLA.LINE_TYPE                 = 'LINE'
                 ) xx,
                 mtl_material_transactions mmt          
              WHERE 1 = 1      
               AND xte.application_id = xe.application_id 
               AND xe.application_id = xeh.application_id 
               AND xeh.application_id = xel.application_id 
               AND xeh.application_id IN ( 707, 222, 200 ) --200 : Payables, 222 : Receivables, 707 : Cost Management 
             AND xte.entity_code IN ( 'MTL_ACCOUNTING_EVENTS', 'TRANSACTIONS', 'AP_INVOICES' )  
        --AND RCTLA.INTERFACE_LINE_CONTEXT    = 'ORDER ENTRY'
        --AND RCTLA.LINE_TYPE                 = 'LINE'
             AND xte.entity_id = xe.entity_id 
             AND xeh.event_id = xe.event_id
             AND xeh.ledger_id = xte.ledger_id
             AND xeh.ae_header_id = xel.ae_header_id 
             AND gcc.CODE_COMBINATION_ID = xel.code_combination_id
             --AND GCC.SEGMENT2 = 'E110001'  
             and mmt.TRX_SOURCE_LINE_ID = yy.LINE_ID(+)
             and yy.LINE_ID=xx.line_id(+)
             and yy.HEADER_ID = xx.HEADER_ID(+) 
             and mmt.transaction_id = xte.source_id_int_1  
             and (NVL (xel.accounted_dr, 0) - NVL (xel.accounted_cr, 0)) <> 0
             AND xte.ledger_id = nvl('{ladger_id}',xte.ledger_id)
             AND xeh.ACCOUNTING_DATE BETWEEN '{from_date}' and '{to_date}'
             AND GCC.SEGMENT1 = NVL('{unit}',GCC.SEGMENT1)  
             AND gcc.segment2|| '.'|| gcc.segment3|| '.'|| gcc.segment4|| '.'|| gcc.segment5 = 'E110001.999999.99999.999'
             and MMT.TRANSACTION_ID is NOT NULL
        UNION ALL     
        --Query for REVENUE calculation (With TRANSACTION_ID)--
                 SELECT rct.org_id, (SELECT hou.NAME
                              FROM hr_operating_units hou
                             WHERE hou.organization_id = rct.org_id) shipping_org,
               apps.xxcns_cntbn_report_pkg.get_organization_name(rct.organization_id) inv_org,
               apps.xxcns_cntbn_report_pkg.get_region (rct.territory_id) region,
               apps.xxcns_cntbn_report_pkg.get_sub_region(rct.territory_id) sub_region,
               apps.xxcns_cntbn_report_pkg.get_branch (rct.territory_id) branch,
               rct.customer_number customer_code, rct.customer_name,
        	   rct.customer_class_code,
        	   (SELECT hca_bill.customer_category_code 
        		FROM   hz_cust_site_uses_all hcs_bill, 
        			   hz_cust_acct_sites_all hca_bill 
        		WHERE  hcs_bill.site_use_id = rct.bill_to_site_use_id
        			   AND hcs_bill.site_use_code = 'BILL_TO' 
        			   AND hca_bill.cust_acct_site_id = hcs_bill.cust_acct_site_id ) customer_category_code,
               rct.attribute6 cusomer_clasification,
               rct.interface_header_attribute1 sales_order_no,
               rct.interface_header_attribute2 sales_order_type,
               (SELECT oha.attribute5
                  FROM oe_order_headers_v oha
                 WHERE oha.order_number = rct.sales_order
                   AND oha.sold_from_org_id = rct.org_id
                   AND order_type = rct.interface_header_attribute2) order_category,
               apps.arpt_sql_func_util.get_salesrep_name_number(rct.primary_salesrep_id,'NAME') sales_persion,
               (SELECT rctta.TYPE
                  FROM ra_cust_trx_types_all rctta
                 WHERE rctta.cust_trx_type_id = rct.cust_trx_type_id
                   AND rctta.org_id = rct.org_id) trx_class,
               apps.xxcns_cntbn_report_pkg.get_dom_ibd (rct.territory_id) dom_ibd,
               (SELECT rctta.description
                  FROM ra_cust_trx_types_all rctta
                 WHERE rctta.cust_trx_type_id = rct.cust_trx_type_id
                   AND rctta.org_id = rct.org_id) transaction_type,
               rct.trx_number transaction_number,
               TO_CHAR (rct.trx_date, 'DD-MON-RRRR') trx_date,
               rct.invoice_currency_code, rct.ct_reference REFERENCE,
               apps.xxcns_cntbn_report_pkg.get_mis_cat(rct.inventory_item_id,rct.interface_line_attribute10,1) mis_cat1,
               apps.xxcns_cntbn_report_pkg.get_mis_cat(rct.inventory_item_id,rct.interface_line_attribute10,2) mis_cat2,
               apps.xxcns_cntbn_report_pkg.get_item_type1(rct.inventory_item_id,rct.interface_line_attribute10) item_type1,
               apps.xxcns_cntbn_report_pkg.get_item_type2(rct.inventory_item_id,rct.interface_line_attribute10) item_type2,
               apps.xxcns_cntbn_report_pkg.get_item_type3(rct.inventory_item_id,rct.interface_line_attribute10) item_type3,
               apps.xxcns_cntbn_report_pkg.get_item_type4(rct.inventory_item_id,rct.interface_line_attribute10) item_type4,
               (SELECT msi.segment1 FROM mtl_system_items_b msi WHERE msi.inventory_item_id = rct.inventory_item_id AND msi.organization_id = rct.interface_line_attribute10) item_name,
               rct.description item_description,
               ABS (rct.transaction_quantity) quantity_invoiced,
               xla.segment1 revenue_unit, 
               xla.rev_acct revenue_account,
               apps.xxcns_cntbn_report_pkg.get_segment2_desc(xla.segment2) revenue_acct_desc,
               NULL sale_amount, NULL excise_amount, 
               --rct.stvat, 
               decode(NVL (net_sale_cal_1 * SIGN (NVL (xla.accounted_dr, 0) - NVL (xla.accounted_cr, 0)), amt),0,0, rct.stvat * SIGN (NVL (xla.accounted_dr, 0) - NVL (xla.accounted_cr, 0))) stvat,
               NULL inclusive_tax,
              /*,NVL( (ABS((NVL(MMT.TRANSACTION_QUANTITY,RCTLA.QUANTITY_INVOICED))*(RCTLA.UNIT_SELLING_PRICE)*NVL(RCTA.EXCHANGE_RATE,1))
                      + nvl(ROUND(((apps.XXCNS_CNTBN_REPORT_PKG.GET_INCLUSIVE_TAX_AMOUNT (RCTLA.customer_trx_line_id))*
                      (ABS(MMT.TRANSACTION_QUANTITY)))/(NVL(RCTLA.QUANTITY_INVOICED,RCTLA.QUANTITY_CREDITED)),2) ,0))*sign(Nvl (xel.accounted_dr, 0) - Nvl (xel.accounted_cr, 0)),
                    (NVL (xdl.UNROUNDED_ACCOUNTED_DR, 0) - NVL (xdl.UNROUNDED_ACCOUNTED_CR, 0))
                  )NET_SALES */
               NVL (  net_sale_cal_1
                    * SIGN (NVL (xla.accounted_dr, 0) - NVL (xla.accounted_cr, 0)),
                    (amt
                    )
                   ) net_sales,
               NULL cogs_unit, NULL cogs_account, NULL cogs_acct_desc,
               NULL cogs_quantity,
               apps.xxcns_cntbn_report_pkg.get_material_cost(rct.transaction_id) material_cost,
               apps.xxcns_cntbn_report_pkg.get_osp_cost (rct.transaction_id) osp_cost,
               apps.xxcns_cntbn_report_pkg.get_resource_cost(rct.transaction_id)resource_cost,
               NULL cogs_amount, rct.transaction_id, rct.attribute2 project_number,
               (SELECT MAX (tax_invoice_num)
                  FROM apps.jai_tax_lines_v jtl
                 WHERE jtl.entity_code LIKE 'TRANSACTIONS'
                   AND jtl.application_id = 222
                   AND jtl.trx_id = rct.customer_trx_id
                   AND jtl.trx_line_id = rct.customer_trx_line_id
                   AND jtl.tax_rate_type NOT LIKE '%ADHOC%') inv_num
        	  , (select (oola.unit_list_price * oola.ordered_quantity) 
        		 from oe_order_lines_all oola, oe_order_headers_all ooha 
        		 where ooha.HEADER_ID=oola.HEADER_ID
        		 and TO_CHAR (oola.line_id) = rct.interface_line_attribute6
        		 and TO_CHAR (ooha.order_number) = rct.interface_header_attribute1
                 and rownum =1 ) lp,
                (select SUBSTR (oha.attribute20, 1, 45) from oe_order_headers_all oha
                 WHERE oha.order_number = rct.sales_order
                   AND oha.sold_from_org_id = rct.org_id
                   AND rownum = 1 ) spcl_inst		   
          FROM (SELECT   NVL (xdl.unrounded_accounted_dr, 0)
                       - NVL (xdl.unrounded_accounted_cr, 0) amt,
                       xeh.ae_header_id, xel.accounted_dr, xel.accounted_cr,
                       xte.source_id_int_1, xdl.source_distribution_id_num_1,
                       xte.ledger_id, xeh.accounting_date, gcc.segment1, gcc.segment2,
                          gcc.segment1|| '.'|| gcc.segment2|| '.'|| gcc.segment3|| '.'|| gcc.segment4|| '.'|| gcc.segment5 rev_acct
                  FROM apps.xla_transaction_entities_upg xte,
                       apps.xla_events xe,
                       apps.xla_ae_headers xeh,
                       apps.xla_ae_lines xel,
                       gl_code_combinations gcc,
                       apps.xla_distribution_links xdl
                 WHERE 1 = 1
                   AND xte.application_id = xe.application_id
                   AND xe.application_id = xeh.application_id
                   AND xeh.application_id = xel.application_id
                   AND xeh.application_id IN (200, 222) --200 : Payables, 222 : Receivables
                   AND xte.entity_code IN ('TRANSACTIONS', 'AP_INVOICES')
                   AND xel.accounting_class_code IN ('REVENUE', 'UNEARNED_REVENUE', 'ITEM EXPENSE')
                   AND xte.entity_id = xe.entity_id
                   AND xeh.event_id = xe.event_id
                   AND xeh.ledger_id = xte.ledger_id
                   AND xeh.ae_header_id = xel.ae_header_id
                   AND gcc.code_combination_id = xel.code_combination_id
        --                  and xeh.AE_HEADER_ID = 124460858
                   AND xdl.source_distribution_type = 'RA_CUST_TRX_LINE_GL_DIST_ALL'
                   AND xdl.ae_line_num = xel.ae_line_num
                   AND xel.application_id = xdl.application_id
                   AND xdl.ae_header_id = xeh.ae_header_id) xla,
               (SELECT rcta.org_id, rcta.customer_trx_id, rcta.sold_to_customer_id, rcta.bill_to_site_use_id,
                       rcta.territory_id, rcta.interface_header_attribute1,
                       rcta.interface_header_attribute2, rcta.primary_salesrep_id,
                       rcta.cust_trx_type_id, rcta.exchange_rate, rcta.trx_number,
                       rcta.trx_date, rcta.invoice_currency_code, rcta.ct_reference,
                       rcta.attribute2, rctlgda.cust_trx_line_gl_dist_id,
                       rctla.interface_line_attribute6 interface_line_attribute6,
                       rctla.customer_trx_line_id, rctla.inventory_item_id,
                       rctla.interface_line_attribute10, rctla.description,
                       rctla.quantity_invoiced, rctla.unit_selling_price,
                       rctla.quantity_credited, rctla.sales_order, ac.attribute6,
                       ac.customer_name, ac.customer_number, ac.customer_class_code, mmt.transaction_id,
                       mmt.organization_id, mmt.transaction_quantity,
                        NVL(ROUND(((apps.xxcns_cntbn_report_pkg.get_vat_amount(rctla.customer_trx_line_id)) * (ABS (mmt.transaction_quantity))) / (NVL (rctla.quantity_invoiced, rctla.quantity_credited)),2),
                           --ROUND(((apps.xxcns_cntbn_report_pkg.get_gst_tax_amount(rctla.customer_trx_line_id)) * (ABS (mmt.transaction_quantity))) / (NVL (rctla.quantity_invoiced,rctla.quantity_credited)),2)
                          ROUND(((apps.xxcns_cntbn_report_pkg.get_gst_tax_amount(rctla.customer_trx_line_id)) * (ABS (mmt.transaction_quantity))) / (NVL (rctla.quantity_invoiced,rctla.quantity_credited)),2)
                                  ) stvat,
                       (ABS((NVL2(mmt.transaction_quantity, apps.inv_convert.inv_um_convert(mmt.inventory_item_id,
                                                                                            NULL,
                                                                                            NVL (ABS (mmt.transaction_quantity),0),
                                                                                            mmt.transaction_uom,
                                                                                            rctla.uom_code,
                                                                                            NULL,
                                                                                            NULL
                                                                                           ),
                                                            rctla.quantity_invoiced
                                 )) * (rctla.unit_selling_price) * NVL (rcta.exchange_rate, 1))
                        + NVL(ROUND(((apps.xxcns_cntbn_report_pkg.get_inclusive_tax_amount(rctla.customer_trx_line_id)) * (ABS (mmt.transaction_quantity)))
                                  / (NVL (rctla.quantity_invoiced, rctla.quantity_credited) ),2),0)
                       ) net_sale_cal_1
                  FROM ra_customer_trx_all rcta,
                       ra_cust_trx_line_gl_dist_all rctlgda,
                       ra_customer_trx_lines_all rctla,
                       ar_customers ac,
                       mtl_material_transactions mmt
                 WHERE 1 = 1
                   AND rcta.customer_trx_id            =  rctla.customer_trx_id
                   AND rcta.org_id                     =  rctla.org_id 
                   AND rctla.customer_trx_line_id = rctlgda.customer_trx_line_id
                   AND rctla.customer_trx_id = rctlgda.customer_trx_id
                   AND rctla.org_id = rctlgda.org_id
                   AND rcta.sold_to_customer_id = ac.customer_id
                   AND rctlgda.account_set_flag = 'N'
                   AND rctlgda.account_class IN ('REV', 'UNEARN')
                   AND mmt.trx_source_line_id = rctla.interface_line_attribute6
                   AND mmt.source_code IN ('ORDER ENTRY', 'RCV')
               ) rct
         WHERE 1 = 1
           AND xla.source_id_int_1 = rct.customer_trx_id(+)
           AND rct.cust_trx_line_gl_dist_id(+) = xla.source_distribution_id_num_1
           AND xla.segment2 in ('R111001', 'R111002', 'R111011', 'R113001', 'R113003', 'R115001', 'R115003', 'R124020')
           AND xla.ledger_id = NVL ('{ladger_id}', xla.ledger_id)
           AND xla.accounting_date BETWEEN '{from_date}' and '{to_date}'
          --AND xla.segment1 = NVL ('{unit}', xla.segment1)
           AND rct.transaction_id IS NOT NULL
        )
        GROUP BY transaction_id) 
        )
        union all
        (SELECT   MAX(org_id) org_id, MAX(shipping_org) shipping_org, MAX(inv_org) inv_org, MAX(region) region, MAX(sub_region) sub_region, MAX(branch) branch,
                  MAX(customer_code) customer_code, MAX(customer_name) customer_name, MAX(customer_class_code) customer_class_code, MAX(customer_category_code) customer_category_code,
        		  MAX(cusomer_clasification) cusomer_clasification, MAX(sales_order_no) sales_order_no,
                   MAX(sales_order_type) sales_order_type,  MAX(order_category) order_category, MAX(sales_persion) sales_persion,  MAX(trx_class) trx_class,  MAX(dom_ibd) dom_ibd,
                   MAX(transaction_type) transaction_type,  MAX(transaction_number) transaction_number,  MAX(trx_date) trx_date,
                   MAX(invoice_currency_code) invoice_currency_code,  MAX(REFERENCE) REFERENCE,  MAX(mis_cat1) mis_cat1,  MAX(mis_cat2) mis_cat2,  MAX(item_type1) item_type1,
                   MAX(item_type2) item_type2,  MAX(item_type3) item_type3,  MAX(item_type4) item_type4, MAX(item_name) item_name, MAX(item_description) item_description,
                   MIN(quantity_invoiced) quantity_invoiced,  MAX(revenue_unit) revenue_unit, MAX(revenue_account) revenue_account, MAX(revenue_acct_desc) revenue_acct_desc,
                   SUM(sale_amount) sale_amount,  SUM(excise_amount) excise_amount,  SUM(stvat) stvat,  SUM(inclusive_tax) inclusive_tax,
                   SUM(net_sales)  net_sales,  MAX(cogs_unit) cogs_unit,  MAX(cogs_account) cogs_account,
                   MAX(cogs_acct_desc) cogs_acct_desc,  MAX(cogs_quantity) cogs_quantity, MAX(material_cost)  material_cost,  MAX(osp_cost) osp_cost,
                   SUM(resource_cost) resource_cost,  SUM(cogs_amount) cogs_amount, max(transaction_id),  MAX(project_number) project_number, max(Inv_Num) GST_INVOICE_NUMBER
        		   ,sum(lp) lp, max(spcl_inst) spcl_inst
        FROM           
        (
          --Query for COGS calculation (Without TRANSACTION_ID)--
               select     YY.ORG_ID
            ,   (select hou.NAME from HR_OPERATING_UNITS HOU where HOU.ORGANIZATION_ID=YY.ORG_ID) SHIPPING_ORG
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_organization_name(MMT.ORGANIZATION_ID) INV_ORG
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_region(NVL(XX.territory_id,YY.territory_id)) REGION
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_sub_region(NVL(XX.territory_id,YY.territory_id)) SUB_REGION
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_branch(NVL(XX.territory_id,YY.territory_id)) BRANCH
            ,   YY.CUSTOMER_NUMBER  CUSTOMER_CODE
            ,   YY.CUSTOMER_NAME
        	,   YY.CUSTOMER_CLASS_CODE
        	,   (SELECT hca_bill.customer_category_code 
        		FROM   hz_cust_site_uses_all hcs_bill, 
        			   hz_cust_acct_sites_all hca_bill 
        		WHERE  hcs_bill.site_use_id = XX.bill_to_site_use_id
        			   AND hcs_bill.site_use_code = 'BILL_TO' 
        			   AND hca_bill.cust_acct_site_id = hcs_bill.cust_acct_site_id ) customer_category_code
            ,   YY.attribute6 cusomer_clasification 
            ,   to_char(yy.order_number) SALES_ORDER_NO
            ,   (select ot.name from  oe_transaction_types_tl ot where ot.transaction_type_id = yy.order_type_id AND ot.LANGUAGE = USERENV ('LANG')) SALES_ORDER_TYPE
            ,   yy.ATTRIBUTE5  ORDER_CATEGORY
            ,   apps.arpt_sql_func_util.get_salesrep_name_number (XX.primary_salesrep_id,'NAME') sales_persion
                ,(select rctta.TYPE from RA_CUST_TRX_TYPES_ALL RCTTA where RCTTA.CUST_TRX_TYPE_ID = XX.CUST_TRX_TYPE_ID and RCTTA.ORG_ID = XX.ORG_ID) TRX_CLASS
                ,apps.XXCNS_CNTBN_REPORT_PKG.get_dom_ibd(NVL(XX.territory_id,YY.territory_id)) DOM_IBD 
                ,(select rctta.DESCRIPTION from RA_CUST_TRX_TYPES_ALL RCTTA where RCTTA.CUST_TRX_TYPE_ID = XX.CUST_TRX_TYPE_ID and RCTTA.ORG_ID = XX.ORG_ID) TRANSACTION_TYPE
                ,XX.TRX_NUMBER TRANSACTION_NUMBER
                ,TO_CHAR(XX.TRX_DATE,'DD-MON-RRRR') TRX_DATE
                ,XX.invoice_currency_code
                ,XX.CT_REFERENCE REFERENCE
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_mis_cat(MMT.INVENTORY_ITEM_ID,MMT.ORGANIZATION_ID,1) MIS_CAT1
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_mis_cat(MMT.INVENTORY_ITEM_ID,MMT.ORGANIZATION_ID,2) MIS_CAT2
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_item_type1(MMT.INVENTORY_ITEM_ID,MMT.ORGANIZATION_ID) ITEM_TYPE1
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_item_type2(MMT.INVENTORY_ITEM_ID,MMT.ORGANIZATION_ID) ITEM_TYPE2
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_item_type3(MMT.INVENTORY_ITEM_ID,MMT.ORGANIZATION_ID) ITEM_TYPE3
            ,   apps.XXCNS_CNTBN_REPORT_PKG.get_item_type4(MMT.INVENTORY_ITEM_ID,MMT.ORGANIZATION_ID) ITEM_TYPE4  
                ,(select MSI.SEGMENT1 from MTL_SYSTEM_ITEMS_B MSI where MSI.INVENTORY_ITEM_ID = MMT.INVENTORY_ITEM_ID and MSI.ORGANIZATION_ID = MMT.ORGANIZATION_ID) ITEM_NAME
                ,YY.DESCRIPTION  ITEM_DESCRIPTION
                ,ABS(MMT.TRANSACTION_QUANTITY) QUANTITY_INVOICED
                ,NULL   REVENUE_UNIT
                ,NULL REVENUE_ACCOUNT
                ,NULL REVENUE_ACCT_DESC
                ,NULL SALE_AMOUNT
                ,NULL EXCISE_AMOUNT
                ,NULL STVAT
                ,NULL INCLUSIVE_TAX
                ,NULL NET_SALES
                ,GCC.SEGMENT1 COGS_UNIT
                ,GCC.SEGMENT1||'.'||GCC.SEGMENT2||'.'||GCC.SEGMENT3||'.'||GCC.SEGMENT4||'.'||GCC.SEGMENT5 COGS_ACCOUNT
                ,apps.XXCNS_CNTBN_REPORT_PKG.get_segment2_desc(GCC.SEGMENT2) COGS_ACCT_DESC
                --,ABS(MMT.TRANSACTION_QUANTITY) COGS_QUANTITY
        		,ABS(case when MMT.TRANSACTION_TYPE_ID = 10008 and MMT.TRANSACTION_ACTION_ID = 36 and MMT.TRANSACTION_SOURCE_TYPE_ID = 2 and MMT.TRANSACTION_SOURCE_NAME is NOT NULL
                  then (select MMT1.TRANSACTION_QUANTITY 
                       from mtl_material_transactions mmt1 
                       where mmt1.transaction_id = (select max(MMT2.TRANSACTION_ID)
                                              from mtl_material_transactions MMT2
                                              where mmt2.TRANSACTION_TYPE_ID = 33 
                                              and mmt2.TRANSACTION_ACTION_ID = 1 
                                              and mmt2.TRANSACTION_SOURCE_TYPE_ID = 2 
                                              and mmt2.TRANSACTION_SOURCE_NAME is NULL
                                              and mmt2.TRANSACTION_SOURCE_ID = mmt.TRANSACTION_SOURCE_ID
                                              and mmt2.TRX_SOURCE_LINE_ID = mmt.TRX_SOURCE_LINE_ID))
                 else  mmt.TRANSACTION_QUANTITY
                 end)  COGS_QUANTITY
                ,apps.XXCNS_CNTBN_REPORT_PKG.GET_MATERIAL_COST(MMT.TRANSACTION_ID) MATERIAL_COST
                ,apps.XXCNS_CNTBN_REPORT_PKG.GET_OSP_COST(MMT.TRANSACTION_ID) OSP_COST
                ,apps.XXCNS_CNTBN_REPORT_PKG.GET_RESOURCE_COST(MMT.TRANSACTION_ID) RESOURCE_COST
                ,(NVL (xel.accounted_dr, 0) - NVL (xel.accounted_cr, 0)) COGS_AMOUNT
                --,MMT.TRANSACTION_ID
                ,(case when MMT.TRANSACTION_TYPE_ID = 10008 and MMT.TRANSACTION_ACTION_ID = 36 and MMT.TRANSACTION_SOURCE_TYPE_ID = 2 and MMT.TRANSACTION_SOURCE_NAME is NOT NULL
                 then (select max(MMT2.TRANSACTION_ID)
                       from mtl_material_transactions MMT2
                       where mmt2.TRANSACTION_TYPE_ID = 33 and mmt2.TRANSACTION_ACTION_ID = 1 and mmt2.TRANSACTION_SOURCE_TYPE_ID = 2 and mmt2.TRANSACTION_SOURCE_NAME is NULL
                       and mmt2.TRANSACTION_SOURCE_ID = mmt.TRANSACTION_SOURCE_ID
                       and mmt2.TRX_SOURCE_LINE_ID = mmt.TRX_SOURCE_LINE_ID)
                 else  mmt.transaction_id
                 end) TRANSACTION_ID
                ,xx.attribute2 PROJECT_NUMBER 
                ,(select max(TAX_INVOICE_NUM)       
                FROM   apps.jai_tax_lines_v jtl 
                WHERE  jtl.entity_code LIKE 'TRANSACTIONS'
                AND jtl.APPLICATION_ID = 222
                AND  jtl.TRX_ID = xx.CUSTOMER_TRX_ID
                AND jtl.trx_line_id = xx.CUSTOMER_TRX_LINE_ID 
                AND jtl.TAX_RATE_TYPE  NOT LIKE '%ADHOC%') Inv_Num
                ,yy.lp ,yy.spcl_inst		
            FROM apps.xla_transaction_entities_upg xte,
                 apps.xla_events xe,
                 apps.xla_ae_headers xeh,
                 apps.xla_ae_lines xel,
                 gl_code_combinations gcc,
                 (select ooha.order_number, ooha.header_id, ooha.order_type_id, OOHA.ATTRIBUTE5, OOLA.ORG_ID, oola.LINE_ID, msi.DESCRIPTION, ARC.CUSTOMER_NUMBER, ARC.CUSTOMER_NAME, ARC.attribute6, ARC.CUSTOMER_CLASS_CODE
                  ,(SELECT terr.territory_id FROM hz_cust_site_uses_all ship_su, ra_territories terr WHERE  ship_su.site_use_id = oola.invoice_to_org_id AND ship_su.territory_id = terr.territory_id) territory_id
        		  ,(oola.unit_list_price * oola.ordered_quantity) lp, SUBSTR (ooha.attribute20, 1, 45) spcl_inst
        		 from oe_order_headers_all ooha,
                 oe_order_lines_all oola,
                 MTL_SYSTEM_ITEMS_B                  MSI,
                 AR_CUSTOMERS                        ARC
                 where 1 = 1
                 AND ooha.HEADER_ID=oola.HEADER_ID
                 and ARC.CUSTOMER_ID = ooha.sold_to_org_id        
                 AND oola.SHIP_FROM_ORG_ID       =   MSI.ORGANIZATION_ID
                 AND oola.INVENTORY_ITEM_ID      =   MSI.INVENTORY_ITEM_ID 
                 ) yy,
                 (select RCTA.attribute2, rcta.CT_REFERENCE, rcta.invoice_currency_code,
                         RCTA.TRX_DATE,RCTA.TRX_NUMBER,RCTA.territory_id,rcta.primary_salesrep_id, rcta.INTERFACE_HEADER_ATTRIBUTE1, rcta.INTERFACE_HEADER_ATTRIBUTE2, 
                         RCTA.CUST_TRX_TYPE_ID, RCTA.BILL_TO_SITE_USE_ID,
                         RCTLA.SALES_ORDER, RCTLA.ORG_ID, RCTLA.SALES_ORDER_LINE, RCTLA.INTERFACE_LINE_ATTRIBUTE6,
                         RCTLA.DESCRIPTION, RCTLA.customer_trx_id, RCTLA.customer_trx_line_id, RCTLA.QUANTITY_INVOICED,RCTLA.QUANTITY_CREDITED, RCTLA.UNIT_SELLING_PRICE,
                         OHA.HEADER_ID, OLA.LINE_ID               
                 from OE_ORDER_HEADERS_ALL                 OHA,
                      OE_ORDER_LINES_ALL                  OLA,
                      RA_CUSTOMER_TRX_LINES_ALL           RCTLA,
                      RA_CUSTOMER_TRX_ALL                 RCTA 
                 WHERE 1 = 1
                 AND RCTA.CUSTOMER_TRX_ID            =  RCTLA.CUSTOMER_TRX_ID
                 AND RCTA.ORG_ID                     =  RCTLA.ORG_ID 
                 AND RCTLA.SALES_ORDER               =   OHA.ORDER_NUMBER
                 AND RCTLA.ORG_ID                    =   OHA.SOLD_FROM_ORG_ID
                 AND RCTLA.SALES_ORDER_LINE          =   OLA.LINE_NUMBER
                 AND RCTLA.INTERFACE_LINE_ATTRIBUTE6 =   to_char(OLA.LINE_ID)
                 AND RCTLA.INTERFACE_LINE_CONTEXT    = 'ORDER ENTRY'
                 AND RCTLA.LINE_TYPE                 = 'LINE'
                 ) xx,
                 mtl_material_transactions mmt   
            WHERE 1 = 1      
               AND xte.application_id = xe.application_id 
               AND xe.application_id = xeh.application_id 
               AND xeh.application_id = xel.application_id 
               AND xeh.application_id IN ( 707, 222, 200 ) --200 : Payables, 222 : Receivables, 707 : Cost Management 
               AND xte.entity_code IN ( 'MTL_ACCOUNTING_EVENTS', 'TRANSACTIONS', 'AP_INVOICES' )  
        --AND RCTLA.INTERFACE_LINE_CONTEXT    = 'ORDER ENTRY'
        --AND RCTLA.LINE_TYPE                 = 'LINE' 
             AND xte.entity_id = xe.entity_id 
             AND xeh.event_id = xe.event_id
             AND xeh.ledger_id = xte.ledger_id
             AND xeh.ae_header_id = xel.ae_header_id 
             AND gcc.CODE_COMBINATION_ID = xel.code_combination_id
             --AND GCC.SEGMENT2 = 'E110001'  
             and mmt.TRX_SOURCE_LINE_ID = yy.LINE_ID(+)
             and yy.LINE_ID=xx.line_id(+)
             and yy.HEADER_ID = xx.HEADER_ID(+) 
             and mmt.transaction_id(+) = xte.source_id_int_1  
             and (NVL (xel.accounted_dr, 0) - NVL (xel.accounted_cr, 0)) <> 0
             AND xte.ledger_id = nvl('{ladger_id}',xte.ledger_id)
             AND xeh.ACCOUNTING_DATE BETWEEN '{from_date}' and '{to_date}'
             --AND GCC.SEGMENT1 =NVL('{unit}',GCC.SEGMENT1)  
             AND gcc.segment2|| '.'|| gcc.segment3|| '.'|| gcc.segment4|| '.'|| gcc.segment5 = 'E110001.999999.99999.999'
             and MMT.TRANSACTION_ID is NULL
        UNION ALL     
        --Query for REVENUE calculation (Without TRANSACTION_ID)--
                SELECT rct.org_id, (SELECT hou.NAME
                              FROM hr_operating_units hou
                             WHERE hou.organization_id = rct.org_id) shipping_org,
               apps.xxcns_cntbn_report_pkg.get_organization_name(rct.organization_id) inv_org,
               apps.xxcns_cntbn_report_pkg.get_region (rct.territory_id) region,
               apps.xxcns_cntbn_report_pkg.get_sub_region(rct.territory_id) sub_region,
               apps.xxcns_cntbn_report_pkg.get_branch (rct.territory_id) branch,
               rct.customer_number customer_code, rct.customer_name, rct.customer_class_code,
        	   (SELECT hca_bill.customer_category_code 
        		FROM   hz_cust_site_uses_all hcs_bill, 
        			   hz_cust_acct_sites_all hca_bill 
        		WHERE  hcs_bill.site_use_id = rct.bill_to_site_use_id
        			   AND hcs_bill.site_use_code = 'BILL_TO' 
        			   AND hca_bill.cust_acct_site_id = hcs_bill.cust_acct_site_id ) customer_category_code,
               rct.attribute6 cusomer_clasification,
               rct.interface_header_attribute1 sales_order_no,
               rct.interface_header_attribute2 sales_order_type,
               (SELECT oha.attribute5
                  FROM oe_order_headers_v oha
                 WHERE oha.order_number = rct.sales_order
                   AND oha.sold_from_org_id = rct.org_id
                   AND order_type = rct.interface_header_attribute2) order_category,
               apps.arpt_sql_func_util.get_salesrep_name_number(rct.primary_salesrep_id,'NAME') sales_persion,
               (SELECT rctta.TYPE
                  FROM ra_cust_trx_types_all rctta
                 WHERE rctta.cust_trx_type_id = rct.cust_trx_type_id
                   AND rctta.org_id = rct.org_id) trx_class,
               apps.xxcns_cntbn_report_pkg.get_dom_ibd (rct.territory_id) dom_ibd,
               (SELECT rctta.description
                  FROM ra_cust_trx_types_all rctta
                 WHERE rctta.cust_trx_type_id = rct.cust_trx_type_id
                   AND rctta.org_id = rct.org_id) transaction_type,
               rct.trx_number transaction_number,
               TO_CHAR (rct.trx_date, 'DD-MON-RRRR') trx_date,
               rct.invoice_currency_code, rct.ct_reference REFERENCE,
               apps.xxcns_cntbn_report_pkg.get_mis_cat(rct.inventory_item_id,rct.interface_line_attribute10,1) mis_cat1,
               apps.xxcns_cntbn_report_pkg.get_mis_cat(rct.inventory_item_id,rct.interface_line_attribute10,2) mis_cat2,
               apps.xxcns_cntbn_report_pkg.get_item_type1(rct.inventory_item_id,rct.interface_line_attribute10) item_type1,
               apps.xxcns_cntbn_report_pkg.get_item_type2(rct.inventory_item_id,rct.interface_line_attribute10) item_type2,
               apps.xxcns_cntbn_report_pkg.get_item_type3(rct.inventory_item_id,rct.interface_line_attribute10) item_type3,
               apps.xxcns_cntbn_report_pkg.get_item_type4(rct.inventory_item_id,rct.interface_line_attribute10) item_type4,
               (SELECT msi.segment1 FROM mtl_system_items_b msi WHERE msi.inventory_item_id = rct.inventory_item_id AND msi.organization_id = rct.interface_line_attribute10) item_name,
               rct.description item_description,
               ABS (rct.transaction_quantity) quantity_invoiced,
               xla.segment1 revenue_unit, 
               xla.rev_acct revenue_account,
               apps.xxcns_cntbn_report_pkg.get_segment2_desc(xla.segment2) revenue_acct_desc,
               NULL sale_amount, NULL excise_amount, 
               --rct.stvat, 
               decode(NVL (net_sale_cal_1 * SIGN (NVL (xla.accounted_dr, 0) - NVL (xla.accounted_cr, 0)), amt),0,0, rct.stvat * SIGN (NVL (xla.accounted_dr, 0) - NVL (xla.accounted_cr, 0))) stvat, 
               NULL inclusive_tax,
              /*,NVL( (ABS((NVL(MMT.TRANSACTION_QUANTITY,RCTLA.QUANTITY_INVOICED))*(RCTLA.UNIT_SELLING_PRICE)*NVL(RCTA.EXCHANGE_RATE,1))
                      + nvl(ROUND(((apps.XXCNS_CNTBN_REPORT_PKG.GET_INCLUSIVE_TAX_AMOUNT (RCTLA.customer_trx_line_id))*
                      (ABS(MMT.TRANSACTION_QUANTITY)))/(NVL(RCTLA.QUANTITY_INVOICED,RCTLA.QUANTITY_CREDITED)),2) ,0))*sign(Nvl (xel.accounted_dr, 0) - Nvl (xel.accounted_cr, 0)),
                    (NVL (xdl.UNROUNDED_ACCOUNTED_DR, 0) - NVL (xdl.UNROUNDED_ACCOUNTED_CR, 0))
                  )NET_SALES */
               NVL (  net_sale_cal_1
                    * SIGN (NVL (xla.accounted_dr, 0) - NVL (xla.accounted_cr, 0)),
                    (amt
                    )
                   ) net_sales,
               NULL cogs_unit, NULL cogs_account, NULL cogs_acct_desc,
               NULL cogs_quantity,
               apps.xxcns_cntbn_report_pkg.get_material_cost(rct.transaction_id) material_cost,
               apps.xxcns_cntbn_report_pkg.get_osp_cost (rct.transaction_id) osp_cost,
               apps.xxcns_cntbn_report_pkg.get_resource_cost(rct.transaction_id)resource_cost,
               NULL cogs_amount, rct.transaction_id, rct.attribute2 project_number,
               (SELECT MAX (tax_invoice_num)
                  FROM apps.jai_tax_lines_v jtl
                 WHERE jtl.entity_code LIKE 'TRANSACTIONS'
                   AND jtl.application_id = 222
                   AND jtl.trx_id = rct.customer_trx_id
                   AND jtl.trx_line_id = rct.customer_trx_line_id
                   AND jtl.tax_rate_type NOT LIKE '%ADHOC%') inv_num
        		,(select (oola.unit_list_price * oola.ordered_quantity) 
        		 from oe_order_lines_all oola, oe_order_headers_all ooha 
        		 where ooha.HEADER_ID=oola.HEADER_ID
        		 and TO_CHAR (oola.line_id) = rct.interface_line_attribute6
        		 and TO_CHAR (ooha.order_number) = rct.interface_header_attribute1) lp,
                (select SUBSTR (oha.attribute20, 1, 45) from oe_order_headers_all oha
                 WHERE oha.order_number = rct.sales_order
                   AND oha.sold_from_org_id = rct.org_id
                   and rownum =1 ) spcl_inst		 
          FROM (SELECT   NVL (xdl.unrounded_accounted_dr, 0)
                       - NVL (xdl.unrounded_accounted_cr, 0) amt,
                       xeh.ae_header_id, xel.accounted_dr, xel.accounted_cr,
                       xte.source_id_int_1, xdl.source_distribution_id_num_1,
                       xte.ledger_id, xeh.accounting_date, gcc.segment1, gcc.segment2,
                          gcc.segment1|| '.'|| gcc.segment2|| '.'|| gcc.segment3|| '.'|| gcc.segment4|| '.'|| gcc.segment5 rev_acct
                  FROM apps.xla_transaction_entities_upg xte,
                       apps.xla_events xe,
                       apps.xla_ae_headers xeh,
                       apps.xla_ae_lines xel,
                       gl_code_combinations gcc,
                       apps.xla_distribution_links xdl
                 WHERE 1 = 1
                   AND xte.application_id = xe.application_id
                   AND xe.application_id = xeh.application_id
                   AND xeh.application_id = xel.application_id
                   AND xeh.application_id IN (200, 222) --200 : Payables, 222 : Receivables
                   AND xte.entity_code IN ('TRANSACTIONS', 'AP_INVOICES')
                   AND xel.accounting_class_code IN ('REVENUE', 'UNEARNED_REVENUE', 'ITEM EXPENSE')
                   AND xte.entity_id = xe.entity_id
                   AND xeh.event_id = xe.event_id
                   AND xeh.ledger_id = xte.ledger_id
                   AND xeh.ae_header_id = xel.ae_header_id
                   AND gcc.code_combination_id = xel.code_combination_id
        --                  and xeh.AE_HEADER_ID = 124460858
                   AND xdl.source_distribution_type = 'RA_CUST_TRX_LINE_GL_DIST_ALL'
                   AND xdl.ae_line_num = xel.ae_line_num
                   AND xel.application_id = xdl.application_id
                   AND xdl.ae_header_id = xeh.ae_header_id) xla,
               (SELECT rcta.org_id, rcta.customer_trx_id, rcta.sold_to_customer_id, rcta.bill_to_site_use_id,
                       rcta.territory_id, rcta.interface_header_attribute1,
                       rcta.interface_header_attribute2, rcta.primary_salesrep_id,
                       rcta.cust_trx_type_id, rcta.exchange_rate, rcta.trx_number,
                       rcta.trx_date, rcta.invoice_currency_code, rcta.ct_reference,
                       rcta.attribute2, rctlgda.cust_trx_line_gl_dist_id,
                       rctla.interface_line_attribute6 interface_line_attribute6, rctla.interface_line_attribute1,
                       rctla.customer_trx_line_id, rctla.inventory_item_id,
                       rctla.interface_line_attribute10, rctla.description,
                       rctla.quantity_invoiced, rctla.unit_selling_price,
                       rctla.quantity_credited, rctla.sales_order, ac.attribute6,
                       ac.customer_name, ac.customer_number, ac.customer_class_code, mmt.transaction_id, 
                       mmt.organization_id, mmt.transaction_quantity,
                       NVL
                          (ROUND
                              (  (  (apps.xxcns_cntbn_report_pkg.get_vat_amount
                                                           (rctla.customer_trx_line_id)
                                    )
                                  * (ABS (NVL(mmt.transaction_quantity,rctla.quantity_invoiced)))
                                 )
                               / (NVL (rctla.quantity_invoiced,
                                       rctla.quantity_credited
                                      )
                                 ),
                               2
                              ),
                           ROUND
                              (  (  (apps.xxcns_cntbn_report_pkg.get_gst_tax_amount
                                                           (rctla.customer_trx_line_id)
                                    )
                                  * (ABS (NVL(mmt.transaction_quantity,rctla.quantity_invoiced)))
                                 )
                               / (NVL (rctla.quantity_invoiced,
                                       rctla.quantity_credited
                                      )
                                 ),
                               2
                              )
                          ) stvat,
                       (  ABS
                             (  (NVL2
                                    (mmt.transaction_quantity,
                                     apps.inv_convert.inv_um_convert
                                                 (mmt.inventory_item_id,
                                                  NULL,
                                                  NVL (ABS (mmt.transaction_quantity),
                                                       0
                                                      ),
                                                  mmt.transaction_uom,
                                                  rctla.uom_code,
                                                  NULL,
                                                  NULL
                                                 ),
                                     rctla.quantity_invoiced
                                    )
                                )
                              * (rctla.unit_selling_price)
                              * NVL (rcta.exchange_rate, 1)
                             )
                        + NVL
                             (ROUND
                                 (  (  (apps.xxcns_cntbn_report_pkg.get_inclusive_tax_amount
                                                           (rctla.customer_trx_line_id)
                                       )
                                     * (ABS (mmt.transaction_quantity))
                                    )
                                  / (NVL (rctla.quantity_invoiced,
                                          rctla.quantity_credited
                                         )
                                    ),
                                  2
                                 ),
                              0
                             )
                       ) net_sale_cal_1
                  FROM ra_customer_trx_all rcta,
                       ra_cust_trx_line_gl_dist_all rctlgda,
                       ra_customer_trx_lines_all rctla,
                       ar_customers ac,
                       mtl_material_transactions mmt
                 WHERE 1 = 1
                   AND rcta.customer_trx_id            =  rctla.customer_trx_id
                   AND rcta.org_id                     =  rctla.org_id 
                   AND rctla.customer_trx_line_id = rctlgda.customer_trx_line_id
                   AND rctla.customer_trx_id = rctlgda.customer_trx_id
                   AND rctla.org_id = rctlgda.org_id
                   AND rcta.sold_to_customer_id = ac.customer_id
                   AND rctlgda.account_set_flag = 'N'
                   AND rctlgda.account_class IN ('REV', 'UNEARN')
                   AND mmt.trx_source_line_id(+) = rctla.interface_line_attribute6 
                   AND mmt.source_code(+) IN ('ORDER ENTRY', 'RCV')
               ) rct
         WHERE 1 = 1
           AND xla.source_id_int_1 = rct.customer_trx_id(+)
           AND rct.cust_trx_line_gl_dist_id(+) = xla.source_distribution_id_num_1
           AND xla.segment2 in ('R111001', 'R111002', 'R111011', 'R113001', 'R113003', 'R115001', 'R115003', 'R124020')
           AND xla.ledger_id = NVL ('{ladger_id}', xla.ledger_id)
           AND xla.accounting_date BETWEEN '{from_date}' and '{to_date}'
           --AND xla.segment1 = NVL ('{unit}', xla.segment1)
           AND rct.transaction_id IS  NULL
        )
        GROUP BY org_id, shipping_org, sales_order_no, transaction_number, revenue_account, cogs_account )
        )
        union all
        select NULL org_id, NULL shipping_org, NULL inv_org, NULL region, NULL sub_region, NULL branch,
                   NULL customer_code, NULL customer_name, NULL customer_class_code, NULL customer_category_code, NULL cusomer_clasification, NULL sales_order_no,
                   NULL sales_order_type,  NULL order_category, NULL sales_persion, NULL trx_class, NULL  dom_ibd,
                   gjh.je_category transaction_type, NULL  transaction_number,  TO_CHAR(trunc(gjh.creation_date),'DD-MON-RRRR') trx_date,
                   gjh.CURRENCY_CODE invoice_currency_code, NULL REFERENCE, NULL mis_cat1, NULL mis_cat2, NULL item_type1,
                   NULL item_type2, NULL item_type3, NULL item_type4,NULL  item_name, NULL item_description,
                   NULL quantity_invoiced, 
                   case when GCC.SEGMENT2 <> 'E110001' then GCC.SEGMENT1 else NULL end revenue_unit, 
                   case when GCC.SEGMENT2 <> 'E110001' then GCC.SEGMENT1||'.'||GCC.SEGMENT2||'.'||GCC.SEGMENT3||'.'||GCC.SEGMENT4||'.'||GCC.SEGMENT5 else NULL end revenue_account,
                   case when GCC.SEGMENT2 <> 'E110001' then apps.XXCNS_CNTBN_REPORT_PKG.get_segment2_desc(GCC.SEGMENT2) else NULL end revenue_acct_desc,
                   NULL sale_amount,  NULL excise_amount, NULL stvat, NULL inclusive_tax,
                   case when GCC.SEGMENT2 <> 'E110001' then (Nvl(gjl.accounted_dr, 0) - Nvl(gjl.accounted_cr, 0)) else NULL end net_sales, 
                   case when GCC.SEGMENT2 = 'E110001' then GCC.SEGMENT1 else NULL end cogs_unit,
                   case when GCC.SEGMENT2 = 'E110001' then GCC.SEGMENT1||'.'||GCC.SEGMENT2||'.'||GCC.SEGMENT3||'.'||GCC.SEGMENT4||'.'||GCC.SEGMENT5 else NULL end cogs_account,
                   case when GCC.SEGMENT2 = 'E110001' then apps.XXCNS_CNTBN_REPORT_PKG.get_segment2_desc(GCC.SEGMENT2) else NULL end cogs_acct_desc, 
                   NULL  cogs_quantity, NULL  material_cost, NULL  osp_cost,
                   NULL resource_cost, 
                   case when GCC.SEGMENT2 = 'E110001' then (Nvl(gjl.accounted_dr, 0) - Nvl(gjl.accounted_cr, 0)) else NULL end  cogs_amount, 
                   NULL  transaction_id, NULL  project_number,null project_name, NULL GST_INVOICE_NUMBER, null , null         
        FROM   gl_je_headers gjh, 
                       gl_je_lines gjl, 
                       gl_code_combinations gcc, 
                       gl.gl_periods glp 
                WHERE  gjh.je_header_id = gjl.je_header_id 
                       AND gjl.code_combination_id = gcc.code_combination_id 
                       AND gjh.period_name = glp.period_name 
                       AND glp.period_set_name='CNS Calendar'
                       AND gjh.je_source = 'Manual' 
                       --AND gjh.je_category = 'Adjustment' 
                       AND gjh.status = 'P' 
                       AND gcc.segment2 in ('R111001', 'R111002', 'R111011', 'R113001', 'R113003', 'R115001', 'R115003', 'R124020', 'E110001')
                       --AND gjh.period_name = 'Mar-19' 
                       AND gjh.ledger_id = Nvl('{ladger_id}', gjh.ledger_id) 
                       --AND GCC.SEGMENT1=NVL('{unit}',GCC.SEGMENT1)
                       --AND gcc.segment1 = '1444'
                       AND glp.START_DATE >= '{from_date}' 
                       AND glp.END_DATE <=  '{to_date}'
        order by SALES_ORDER_NO nulls last, transaction_id
    """
    cur = cursor_ora.execute(list_data)
    contribution_report = cur.fetchall()
    print(contribution_report,'oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo')
    df = pd.DataFrame(contribution_report)

    print(df)
    csv_data = df.to_csv(index=False)
    df.to_csv(f'{TABLE_NAME}.csv', index=False)
    print(df, 'ffffffffffffffffff')
    # insert_table_data = f'''\COPY {TABLE_NAME} FROM
    # '{TABLE_NAME}.csv'  CSV HEADER;'''
    # print(insert_table_data,'ddddddddddddddddddddddddddddddddddd')
    remove_none = str(contribution_report).replace("None", "''")
    res = remove_none[1:-1]
    conn_db = psycopg2.connect(user="oracle_user", password="password", host="127.0.0.1", port="5433",database="oracle_db")
    cursor = conn_db.cursor()
    try:
        if table_type == 'create_table':
            print(table_type)
            try:
                cursor.execute(table_create)
                conn_db.commit()
                return JsonResponse({"Message": f" Table  {TABLE_NAME} Created  Successfully"})
            except Exception as e:
                return JsonResponse({"Error": e})
        if table_type == 'insert':
            print(table_type,'table_typetable_typetable_type')
            try:
                # sql_stat = f"""INSERT INTO {TABLE_NAME}  (org_id,
                #             shipping_org,
                #             inv_org,
                #             region,
                #             sub_region,
                #             branch,
                #             customer_code,
                #             customer_name,
                #             customer_class_code,
                #             customer_category_code,
                #             cusomer_clasification,
                #             sales_order_no,
                #             sales_order_type,
                #             order_category,
                #             sales_persion,
                #             trx_class,
                #             dom_ibd,
                #             transaction_type,
                #             transaction_number,
                #             trx_date,
                #             invoice_currency_code,
                #             REFERENCE,
                #             mis_cat1,
                #             mis_cat2,
                #             item_type1,
                #             item_type2,
                #             item_type3,
                #             item_type4,
                #             item_name,
                #             item_description,
                #             quantity_invoiced,
                #             revenue_unit,
                #             revenue_account,
                #             revenue_acct_desc,
                #             sale_amount,
                #             excise_amount,
                #             stvat,
                #             inclusive_tax,
                #             net_sales,
                #             cogs_unit,
                #             cogs_account,
                #             cogs_acct_desc,
                #             cogs_quantity,
                #             material_cost,
                #             osp_cost,
                #             resource_cost,
                #             cogs_amount,
                #             transaction_id,
                #             project_number,
                #             project_name,
                #             GST_INVOICE_NUMBER,
                #             lp,
                #             spcl_inst) VALUES {res} """
                f''' \COPY {TABLE_NAME} FROM '{TABLE_NAME}.csv'  CSV HEADER; '''
                print('sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
                # cursor.execute(f'''\COPY {TABLE_NAME} FROM  '{TABLE_NAME}.csv'  CSV HEADER;''')
                # conn_db.commit()
                # print(conn_db)
                return JsonResponse({"Message": f" In  {TABLE_NAME},  Data inserted  Successfully!!!"})
            except Exception as e:
                return JsonResponse({"Error": e})
        if table_type == 'create&insert':
            print(table_type,'llllllllllllllllll')
        try:
            cursor.execute(table_create)
            conn_db.commit()
            print(cursor,'eeeeeeeeeeeeeeeeeeeeeee')
            # sql_stat = f"""INSERT INTO {TABLE_NAME}  (org_id,
            #             shipping_org,
            #             inv_org,
            #             region,
            #             sub_region,
            #             branch,
            #             customer_code,
            #             customer_name,
            #             customer_class_code,
            #             customer_category_code,
            #             cusomer_clasification,
            #             sales_order_no,
            #             sales_order_type,
            #             order_category,
            #             sales_persion,
            #             trx_class,
            #             dom_ibd,
            #             transaction_type,
            #             transaction_number,
            #             trx_date,
            #             invoice_currency_code,
            #             REFERENCE,
            #             mis_cat1,
            #             mis_cat2,
            #             item_type1,
            #             item_type2,
            #             item_type3,
            #             item_type4,
            #             item_name,
            #             item_description,
            #             quantity_invoiced,
            #             revenue_unit,
            #             revenue_account,
            #             revenue_acct_desc,
            #             sale_amount,
            #             excise_amount,
            #             stvat,
            #             inclusive_tax,
            #             net_sales,
            #             cogs_unit,
            #             cogs_account,
            #             cogs_acct_desc,
            #             cogs_quantity,
            #             material_cost,
            #             osp_cost,
            #             resource_cost,
            #             cogs_amount,
            #             transaction_id,
            #             project_number,
            #             project_name,
            #             GST_INVOICE_NUMBER,
            #             lp,
            #             spcl_inst ) VALUES {res}"""

            print('sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
            cursor.execute(f'''\COPY {TABLE_NAME} FROM  '{TABLE_NAME}.csv'  CSV HEADER;''')
            conn_db.commit()
            print(conn_db,'sssssssssssssssssssssssssssssssssswwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
            # a = " \COPY contribution_report_data4 FROM  'C:\Users\harshita.agarwal\Desktop\Django\DumpReporting_Project\contribution_report_27feb1.csv' CSV HEADER; "
            # print(a,'ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
            return JsonResponse({"Message": f" Table {TABLE_NAME} Created & Data inserted  Successfully!!!"})
        except Exception as e:
            return JsonResponse({"Error": e})

        if table_type=='replace':
            print(table_type)
            try:
                drop_table = f"DROP TABLE {REPLACE_TABLE_NAME}"
                cursor.execute(drop_table)
                conn_db.commit()
                cursor.execute(table_create)
                conn_db.commit()
                sql_stat = f"""INSERT INTO {TABLE_NAME} (org_id,
                            shipping_org,
                            inv_org,
                            region,
                            sub_region,
                            branch,
                            customer_code,
                            customer_name,
                            customer_class_code,
                            customer_category_code,
                            cusomer_clasification,
                            sales_order_no,
                            sales_order_type,
                            order_category,
                            sales_persion,
                            trx_class,
                            dom_ibd,
                            transaction_type,
                            transaction_number,
                            trx_date,
                            invoice_currency_code,
                            REFERENCE,
                            mis_cat1,
                            mis_cat2,
                            item_type1,
                            item_type2,
                            item_type3,
                            item_type4,
                            item_name,
                            item_description,
                            quantity_invoiced,
                            revenue_unit,
                            revenue_account,
                            revenue_acct_desc,
                            sale_amount,
                            excise_amount,
                            stvat,
                            inclusive_tax,
                            net_sales,
                            cogs_unit,
                            cogs_account,
                            cogs_acct_desc,   
                            cogs_quantity,   
                            material_cost,
                            osp_cost,
                            resource_cost,
                            cogs_amount,
                            transaction_id,
                            project_number,
                            project_name,
                            GST_INVOICE_NUMBER,
                            lp,
                            spcl_inst )
                            VALUES {res}"""
                cursor.execute(sql_stat)
                conn_db.commit()
                return JsonResponse({"Message": f"Table {REPLACE_TABLE_NAME} removed and "
                                                f"Table  {TABLE_NAME} Created  & Data inserted  Successfully!!!"})
            except Exception as e:
                return JsonResponse({"Error": e})
#
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table", error)
    context = {
        "contribution_report": contribution_report
    }
    return render(request, 'app/app/contribution_report_data_get.html')

@api_view(['POST'])
def download_contribution_report(request):
    '''
    Download the report from postgres database
    :param request:
    :return:
    '''
    data = request.data
    report_type = data['report_type']
    ladger_id = data['ladger_id']
    unit = data['unit']
    from_date = data['from_date']
    to_date = data['to_date']
    cursor = connection.cursor()
    sql_statement = f'''SELECT * FROM  public.{TABLE_NAME} ;
   -- WHERE (to_date(trx_date,'DD-MON-YY') between 
    --'{from_date}' and  '{to_date}');

    --('{from_date}'='' OR from_date = '{from_date}')
    --and ('{to_date}'='' OR to_date = '{to_date}')
    --and ('{unit}'='' OR unit = '{unit}')
   -- and ('{ladger_id}'='' OR ladger_id = '{ladger_id}');
'''

    cursor.execute(sql_statement)
    row_data = cursor.fetchall()
    output = BytesIO()
    if report_type == 'excel':
        workbook = xlsxwriter.Workbook(output, {'constant_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})
        headings = ['org_id','shipping_org',
                            'inv_org',
                            'region',
                            'sub_region',
                            'branch',
                            'customer_code',
                            'customer_name',
                            'customer_class_code',
                            'customer_category_code',
                            'cusomer_clasification',
                            'sales_order_no',
                            'sales_order_type',
                            'order_category',
                            'sales_persion',
                            'trx_class',
                            'dom_ibd',
                            'transaction_type',
                            'transaction_number',
                            'trx_date',
                            'invoice_currency_code',
                            'REFERENCE',
                            'mis_cat1',
                            'mis_cat2',
                            'item_type1',
                            'item_type2',
                            'item_type3',
                            'item_type4',
                            'item_name',
                            'item_description',
                            'quantity_invoiced',
                            'revenue_unit',
                            'revenue_account',
                            'revenue_acct_desc',
                            'sale_amount',
                            'excise_amount',
                            'stvat',
                            'inclusive_tax',
                            'net_sales',
                            'cogs_unit',
                            'cogs_account',
                            'cogs_acct_desc',
                            'cogs_quantity',
                            'material_cost',
                            'osp_cost',
                            'resource_cost',
                            'cogs_amount',
                            'transaction_id',
                            'project_number',
                            'project_name',
                            'GST_INVOICE_NUMBER',
                            'lp',
                            'spcl_inst']
        col = 0
        for row, data in enumerate(row_data):
            worksheet.write_row('A1', headings, bold)
            worksheet.write_row(row+1, col, data)
        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        return response
    if report_type == 'pdf':
        return HttpResponse("PENDING")

def contribution_report_download_parameter(request):
    '''
    Front view  to download the report
    :param request:
    :return:
    '''
    form = ContributionReportDownload(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        form.save()
        return redirect('')
    else:
        print(form.errors)
    return render(request, 'app/app/contribution_report_download_parameter.html', {'form': form})