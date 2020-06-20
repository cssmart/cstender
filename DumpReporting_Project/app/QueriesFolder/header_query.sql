select
          --distinct
            a.party_name customer_name, hzca.account_number customer_number,
   hzca.customer_class_code customer_type, b.bill_to_customer_id customer_id, b.invoice_currency_code curr_code,
            b.BILL_TO_SITE_USE_ID customer_site_id
           From
                hz_parties A, hz_cust_accounts hzca,
                ra_customer_trx_all B,
                ar_payment_schedules_all C --added on 13n
           Where a.party_id = hzca.party_id
           AND ( hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id))
              )
           AND 	NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
           AND   NVL(b.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(b.BILL_TO_SITE_USE_ID,'99999999999999'))
           AND	b.bill_to_customer_id = hzca.cust_account_id
           AND 	to_date(b.trx_date,'DD-MON-RRRR') <= to_date('{p_end_date}','DD-MON-RRRR')
           AND 	b.complete_flag = 'Y'
           AND c.customer_trx_id = b.customer_trx_id --added on 13n
           AND       b.org_id='{p_org_id}'
           --group By a.customer_name, a.customer_number, --b.invoice_currency_code
           UNION
           Select
           --distinct
           a.party_name customer_name, hzca.account_number customer_number,
           hzca.customer_class_code customer_type, b.pay_from_customer customer_id, b.currency_code curr_code,
            D.CUSTOMER_SITE_USE_ID customer_site_id
           From
               hz_parties A, hz_cust_accounts hzca,
               ar_cash_receipts_all B,
             ar_cash_receipt_history_all C,
             ar_payment_schedules_all D --added on 13n
           Where a.party_id = hzca.party_id
           AND ( hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id))
                )
           AND NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
            AND  NVL(D.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(D.CUSTOMER_SITE_USE_ID,'99999999999999'))
           AND    b.pay_from_customer = hzca.cust_account_id
           AND    to_date(b.receipt_date,'DD-MON-RRRR')    <= to_date('{p_end_date}','DD-MON-RRRR') --Replaced gl_date with Receipt_date for bug#8459757 by JMEENA
           AND b.cash_receipt_id =c.cash_receipt_id
           AND d.cash_receipt_id = b.cash_receipt_id --added on 13n
           AND c.reversal_gl_date is null
           AND b.org_id='{p_org_id}'
           --group By a.customer_name, a.customer_number,
           --b.currency_code

           UNION
           Select
           --distinct
           a.party_name customer_name, hzca.account_number /*a.party_number*/ customer_number, /*Changes by nprashar for bug bug # 7256288*/
           hzca.customer_class_code customer_type,  b.pay_from_customer customer_id, b.currency_code curr_code ,
             C.CUSTOMER_SITE_USE_ID customer_site_id
           From
               hz_parties A, hz_cust_accounts hzca,
               ar_cash_receipts_all B,
           ar_payment_schedules_all C
           Where a.party_id = hzca.party_id
           AND  (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id )))
           AND       NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
           AND  NVL(C.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(C.CUSTOMER_SITE_USE_ID,'99999999999999'))
           AND    b.pay_from_customer = hzca.cust_account_id
           AND    to_date(b.reversal_date,'DD-MON-RRRR')      <= to_date('{p_end_date}','DD-MON-RRRR')
           AND c.cash_receipt_id =  b.cash_receipt_id --added on 13n
           AND       b.org_id='{p_org_id}'
           --group By a.customer_name, a.customer_number,
           --b.currency_code
           ----Query added for adjustment entries by sridhar on 14nov-00
           UNION
           SELECT
           A.party_name customer_name,
           hzca.account_number/*A.party_number*/ customer_number, /*Changes by nprashar for bug bug # 7256288*/
           hzca.customer_class_code customer_type,
           C.bill_to_customer_id customer_id,
           C.invoice_currency_code curr_code ,
            C.BILL_TO_SITE_USE_ID customer_site_id
           FROM
           hz_parties a, hz_cust_accounts hzca ,
           ar_adjustments_all b, ra_customer_trx_all c, ar_payment_schedules_all d
           WHERE     a.party_id = hzca.party_id
           AND    (  hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
           AND   NVL(C.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(C.BILL_TO_SITE_USE_ID,'99999999999999'))
           AND       NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
           AND     b.customer_trx_id = c.customer_trx_id
           /*AND b.customer_trx_id not in (select customer_trx_id from ar_adjustments_all where CHARGEBACK_CUSTOMER_TRX_ID is not NULL or created_from = 'REVERSE_CHARGEBACK')*/ /*added by abezgam for bug#10228717*/
           /*Commented NOT IN and replaced with NOT EXISTS by mmurtuza for bug 14062515*/
           AND NOT EXISTS (
                     SELECT 'x'
                       FROM ar_adjustments_all
                      WHERE (   chargeback_customer_trx_id IS NOT NULL
                             OR created_from = 'REVERSE_CHARGEBACK'
                            )
                        AND customer_trx_id = b.customer_trx_id)
           AND     c.bill_to_customer_id = hzca.cust_account_id
           AND     to_date(b.apply_date,'DD-MON-RRRR') <= to_date('{p_end_date}','DD-MON-RRRR')
           AND     b.status = 'A'
           AND    b.customer_trx_id = d.customer_trx_id
           AND       c.org_id='{p_org_id}'
           ORDER BY 4
