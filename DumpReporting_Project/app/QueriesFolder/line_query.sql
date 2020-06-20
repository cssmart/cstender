select
        trx_number,
        trx_date,
        TYPE,
        reference,
        func_dr_amt(TYPE,amount,amount_other_currency)func_dr_amt,
        func_cr_amt(TYPE,amount,amount_other_currency)func_cr_amt,
        remarks
        from (
        Select
       hzca.cust_account_id  customer_id,
        B.BILL_TO_SITE_USE_ID customer_site_id,
       hzca.account_number customer_number   ,
       a.party_name   customer_name                             ,
       d.gl_date                                                ,
       B.CUSTOMER_TRX_ID                                        ,
       b.trx_number                                             ,
       (SELECT interface_line_Attribute1
       FROM ra_customer_Trx_lines_All
       where CUSTOMER_TRX_ID=b.CUSTOMER_TRX_ID
       and org_id=b.org_id
       and rownum=1)reference,
       TO_CHAR(b.trx_date, 'DD-MM-YYYY') trx_date               ,
       NULL receipt_number                                      ,
       NULL receipt_date                                        ,
       SUBSTR(b.comments,1,50) remarks                          ,
       d.code_combination_id account_id                         ,
       b.invoice_currency_code currency_code                    ,
       b.exchange_rate                                          ,
       d.amount amount                                          ,
       (d.amount * NVL(b.exchange_rate,1)) amount_other_currency,
       F.TYPE                                          ,
       xxcns_deb_led_get_narration(F.TYPE,F.NAME,B.CUSTOMER_TRX_ID)naration,
       b.customer_trx_id                                        ,
       d.customer_trx_line_id                                   ,
       b.rowid
       From
          hz_parties                                           a,
          hz_cust_accounts                                     hzca,
          ra_customer_trx_ALL                                  B,
          RA_CUST_TRX_LINE_GL_DIST_ALL                         D,
          GL_CODE_COMBINATIONS                                 E,
          RA_CUST_TRX_TYPES_ALL                                F,
          ar_payment_schedules_all                             G,
          hz_locations                                         loc,
          hz_party_sites                                       party_site,
          hz_cust_acct_sites_all                               acct_site,
          hz_cust_site_uses_all                                site
       Where a.party_id = hzca.party_id
       AND   b.bill_to_customer_id = hzca.cust_account_id
       AND      b.complete_flag       = 'Y'
       AND     d.customer_trx_id     = b.customer_trx_id
       AND     d.account_class       = 'REC'
       AND     e.code_combination_id = d.code_combination_id
       AND    f.cust_trx_type_id    = b.cust_trx_type_id
       AND     f.type in ('INV','CM','DM','DEP')
       AND     d.latest_rec_flag     = 'Y'
       AND     g.customer_trx_id     = b.customer_trx_id
       and   loc.location_id       = party_site.location_id
       and   party_site.party_site_id    = acct_site.party_site_id
       and   acct_site.cust_acct_site_id = site.cust_acct_site_id
       and   site.site_use_id            = g.customer_site_use_id
       AND     b.org_id              ='{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(b.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(b.BILL_TO_SITE_USE_ID,'99999999999999'))
       AND      (g.gl_date) between  ('{p_start_date}')  AND ('{p_end_date}')
       AND b.invoice_currency_code='INR'
       and     g.payment_schedule_id in
       (select min(payment_schedule_id)
        from   ar_payment_schedules_all
        where  customer_trx_id = g.customer_trx_id)
       UNION ALL
       -- Following Query for Cash receipts
       Select
       hzca.cust_account_id customer_id,
        F.CUSTOMER_SITE_USE_ID customer_site_id ,
       hzca.account_number  customer_number   ,
       a.party_name customer_name                               ,
       e.gl_date                                                ,
       0                                                        ,
       b.receipt_number                                                   ,
       NULL                                                     ,
       TO_CHAR(b.receipt_date,  'DD-MM-YYYY'),
       b.receipt_number                                        ,
       TO_CHAR(b.receipt_date,  'DD-MM-YYYY')                   ,
       NULL                                                     ,
       d.cash_ccid account_id                                   ,
       b.currency_code                                          ,
       b.exchange_rate                                          ,
       b.amount  amount                                         ,
       (b.amount * NVL(b.exchange_rate,1)) amount_other_currency,
       'REC' type                                               ,
       'Amount Received' naration,
       0                                                        ,
       0                                                        ,
       b.rowid
       From
           hz_parties a, hz_cust_accounts hzca,
           ar_cash_receipts_all                                B,
           gl_code_combinations                                C,
           ar_receipt_method_accounts_all                      D,
           ar_cash_receipt_history_all                         E,
                   ar_payment_schedules_all                            F
       Where a.party_id = hzca.party_id
       AND b.pay_from_customer                     = hzca.cust_account_id
       AND    b.remit_bank_acct_use_id            = d.remit_bank_acct_use_id
       AND         d.receipt_method_id                     = b.receipt_method_id
       AND    d.cash_ccid                             = c.code_combination_id
       AND         e.cash_receipt_id                       = b.cash_receipt_id
       AND E.cash_receipt_history_id in (SELECT    min(incrh.cash_receipt_history_id)
                                                     FROM    ar_cash_receipt_history_all incrh
                                                     WHERE   incrh.cash_receipt_id = B.cash_receipt_id
                                                     AND     incrh.status <> 'REVERSED' )
       AND     f.cash_receipt_id                           = b.cash_receipt_id
       AND     b.org_id                                   ='{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999'))
       AND    (e.gl_date) between ('{p_start_date}')  AND ('{p_end_date}')
       AND b.currency_code ='INR'
       UNION ALL
       -- Following Query for Receipt WriteOff
       Select
       hzca.cust_account_id customer_id  ,
        F.CUSTOMER_SITE_USE_ID customer_site_id                          ,
       hzca.account_number  customer_number,
       a.party_name customer_name ,
       g.gl_date     ,
       0                                                                ,
       b.receipt_number                                                             ,
       NULL ,
       TO_CHAR(b.receipt_date,  'DD-MM-YYYY'),
       b.receipt_number                                                 ,
       TO_CHAR(b.receipt_date,  'DD-MM-YYYY')                           ,
       NULL                                                             ,
       d.cash_ccid account_id                                           ,
       b.currency_code                                                  ,
       b.exchange_rate                                                  ,
       g.amount_applied  amount                                         ,
       (g.amount_applied * NVL(b.exchange_rate,1)) amount_other_currency,
       'W/O' type                                                       ,
       xxcns_deb_led_get_narration(TYPE,NULL,0)naration,
       0                                                                ,
       0                                                                ,
       b.rowid
       From
           hz_parties a, hz_cust_accounts hzca ,
           ar_cash_receipts_all                                        B,
           gl_code_combinations                                        C,
           ar_receipt_method_accounts_all                              D,
           ar_cash_receipt_history_all                                 E,
               ar_payment_schedules_all                                    F,
               ar_receivable_applications_all                              G
       Where a.party_id = hzca.party_id
       AND b.pay_from_customer                     = hzca.cust_account_id
       AND g.applied_payment_schedule_id           = -3
       AND g.cash_receipt_id                       = b.cash_receipt_id
       and g.cash_receipt_history_id               = e.cash_receipt_history_id
       AND g.status                                = 'ACTIVITY'
       AND    b.remit_bank_acct_use_id                = d.remit_bank_acct_use_id
       AND d.receipt_method_id                     = b.receipt_method_id
       AND    d.cash_ccid                             = c.code_combination_id
       AND e.cash_receipt_id                       = b.cash_receipt_id
       AND f.cash_receipt_id                       = b.cash_receipt_id
       AND b.org_id                                ='{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999'))
       AND    (g.gl_date)  between ('{p_start_date}')  AND ('{p_end_date}')
       AND b.currency_code ='INR'
       and not exists
       (select 1
        from   ar_cash_receipt_history_all
        where  cash_receipt_id = b.cash_receipt_id
        and    status = 'REVERSED'
        )
       UNION ALL
       -- Following Query for Receipt WriteOff ======================================================================================
       Select
       hzca.cust_account_id customer_id  ,
        F.CUSTOMER_SITE_USE_ID customer_site_id                          ,
       hzca.account_number customer_number           ,
       a.party_name customer_name                                       ,
       g.gl_date     ,
       0                                                                ,
       b.receipt_number                                                            ,
       NULL ,
       TO_CHAR(b.receipt_date,  'DD-MM-YYYY')                                                       ,
       b.receipt_number                                                 ,
       TO_CHAR(b.receipt_date,  'DD-MM-YYYY')                           ,
       NULL                                                             ,
       d.cash_ccid account_id                                           ,
       b.currency_code                                                  ,
       b.exchange_rate                                                  ,
       g.amount_applied  amount                                         ,
       (g.amount_applied * NVL(b.exchange_rate,1)) amount_other_currency,
       'REF' type                                                       ,
       xxcns_deb_led_get_narration(TYPE,NULL,0)naration,
       0                                                                ,
       0                                                                ,
       b.rowid
       From
           hz_parties a, hz_cust_accounts hzca ,
           ar_cash_receipts_all                                        B,
           gl_code_combinations                                        C,
           ar_receipt_method_accounts_all                              D,
           ar_cash_receipt_history_all                                 E,
               ar_payment_schedules_all                                    F,
               ar_receivable_applications_all                              G
       Where a.party_id = hzca.party_id
       AND b.pay_from_customer                     = hzca.cust_account_id
       AND g.applied_payment_schedule_id           = -8
       AND g.cash_receipt_id                       = b.cash_receipt_id
       and g.cash_receipt_history_id               = e.cash_receipt_history_id
       AND g.status                                = 'ACTIVITY'
       AND    b.remit_bank_acct_use_id                = d.remit_bank_acct_use_id
       AND d.receipt_method_id                     = b.receipt_method_id
       AND    d.cash_ccid                             = c.code_combination_id
       AND e.cash_receipt_id                       = b.cash_receipt_id
       AND f.cash_receipt_id                       = b.cash_receipt_id
       AND b.org_id                                ='{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999'))
       AND    (g.gl_date)  between ('{p_start_date}')  AND ('{p_end_date}')
       AND b.currency_code ='INR'
       and not exists
       (select 1
        from   ar_cash_receipt_history_all
        where  cash_receipt_id = b.cash_receipt_id
        and    status = 'REVERSED'
        )
       UNION ALL
       -- Following Query for Receipt Reversal ===========================================================================
       Select
       hzca.cust_account_id customer_id ,
        F.CUSTOMER_SITE_USE_ID customer_site_id,
       hzca.account_number customer_number           ,
       a.party_name customer_name                                       ,
       e.gl_date gl_date                                                ,
       0                                                                ,
       b.receipt_number ,
       NULL                                                             ,
       to_char(e.trx_date,'DD-MM-YYYY')  trx_date                       ,
       b.receipt_number                                                 ,
       TO_CHAR(b.receipt_date,  'DD-MM-YYYY')                           ,
       NULL                                                             ,
       c.code_combination_id account_id                                 ,
       b.currency_code                                                  ,
       b.exchange_rate                                                  ,
       b.amount amount                                                  ,
       (b.amount * NVL(b.exchange_rate,1)) amount_other_currency        ,
       'REV' type                                                       ,
       'Amount Reversed' naration,
       0                                                                ,
       0                                                                ,
       b.rowid
       From
           hz_parties a, hz_cust_accounts hzca ,
           ar_cash_receipts_all                                        B,
           gl_code_combinations                                        C,
           ar_receipt_method_accounts_all                              D,
           ar_cash_receipt_history_all                                 E,
               ar_payment_schedules_all                                    F
       Where a.party_id = hzca.party_id
       AND b.pay_from_customer                       = hzca.cust_account_id
       AND    b.remit_bank_acct_use_id                = d.remit_bank_acct_use_id
       AND d.receipt_method_id                     = b.receipt_method_id
       AND    d.cash_ccid                             = c.code_combination_id
       AND e.cash_receipt_id                       = b.cash_receipt_id
       AND f.cash_receipt_id                       = b.cash_receipt_id
       AND b.org_id                                = '{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999'))
       AND e.status                                = 'REVERSED'
       AND    (e.gl_date) between ('{p_start_date}')  AND ('{p_end_date}')
       AND b.currency_code ='INR'
       and b.reversal_date is not null
       UNION ALL
       -- Following Query for Adjustments===================================================================
       SELECT
       HZCA.CUST_ACCOUNT_ID CUSTOMER_ID  ,
        C.BILL_TO_SITE_USE_ID customer_site_id                               ,
       hzca.account_number  CUSTOMER_NUMBER           ,
       A.PARTY_NAME CUSTOMER_NAME                                       ,
       B.GL_DATE                                                        ,
       0                                                                ,
       B.ADJUSTMENT_NUMBER                                              ,
       NULL,
       TO_CHAR(B.APPLY_DATE,'DD-MM-YYYY') trx_date                      ,
       NULL receipt_number                                              ,
       NULL receipt_date                                                ,
       SUBSTR(b.comments,1,50) remarks                                  ,
       b.code_combination_id account_id                                 ,
       c.invoice_currency_code currency_code                            ,
       c.exchange_rate                                                  ,
       b.amount amount                                                  ,
       (b.amount*NVL(c.exchange_rate,1)) amount_other_currency          ,
       'ADJ' type                                                       ,
       xxcns_deb_led_get_narration(TYPE,NULL,0)naration,
       0                                                                ,
       0                                                                ,
       b.rowid
       FROM
       HZ_PARTIES A, HZ_CUST_ACCOUNTS HZCA,
       ar_adjustments_all                                              b,
       ra_customer_trx_all                                             c,
       ar_payment_schedules_all                                        d,
       gl_code_combinations                                            e
       WHERE
            b.customer_trx_id                         = c.customer_trx_id
       AND a.party_id                              = hzca.party_id
       AND c.bill_to_customer_id                   = hzca.cust_account_id
       AND b.status                                = 'A'
       AND    e.code_combination_id                   = b.code_combination_id
       AND    b.payment_schedule_id                   = d.payment_schedule_id
       AND    b.customer_trx_id                       = d.customer_trx_id
       AND c.org_id                                ='{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(C.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(C.BILL_TO_SITE_USE_ID,'99999999999999'))
       AND    (b.gl_date) between ('{p_start_date}')  AND ('{p_end_date}')
       AND c.invoice_currency_code ='INR'
       AND b.customer_trx_id not in (select customer_trx_id from ar_adjustments_all where CHARGEBACK_CUSTOMER_TRX_ID is not NULL or created_from = 'REVERSE_CHARGEBACK') /*added by abezgam for bug#10228717*/
       UNION ALL   ----comment by zakaul  UNION ALL
       -- -- Following Query for Discounts============================================================
       Select
       hzca.cust_account_id customer_id,
        B.BILL_TO_SITE_USE_ID customer_site_id                                        ,
       hzca.account_number  customer_number                 ,
       a.party_name customer_name                                              ,
       d.gl_date                                                               ,
       B.CUSTOMER_TRX_ID                                                       ,
       b.trx_number                                                            ,
       (SELECT interface_line_Attribute1
       FROM ra_customer_Trx_lines_All
       where CUSTOMER_TRX_ID=b.CUSTOMER_TRX_ID
       and org_id=b.org_id
       and rownum=1)reference,
       TO_CHAR(b.trx_date, 'DD-MM-YYYY') trx_date                              ,
       NULL receipt_number                                                     ,
       NULL receipt_date                                                       ,
       SUBSTR(b.comments,1,50) remarks                                         ,
       earned_discount_ccid account_id                                                            ,
        b.invoice_currency_code currency_code                                  ,
       b.exchange_rate                                                         ,
       d.EARNED_discount_taken amount                                          ,
       d.ACCTD_EARNED_DISCOUNT_TAKEN  amount_other_currency ,
       'DSC' type                                                              ,
       'Cash Discount' naration,
       b.customer_trx_id                                                       ,
       0                                                                       ,
       b.rowid
       From
           hz_parties a, hz_cust_accounts hzca ,
           ra_customer_trx_all                                                B,
           ar_receivable_applications_all                                     D
       Where a.party_id = hzca.party_id
       AND b.bill_to_customer_id                   = hzca.cust_account_id
       AND    b.complete_flag                         = 'Y'
       AND D.EARNED_DISCOUNT_TAKEN                 is not null
       and D.EARNED_DISCOUNT_TAKEN                 <> 0
       AND b.org_id                                = '{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(b.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(b.BILL_TO_SITE_USE_ID,'99999999999999'))
       and b.customer_trx_id                       = d.applied_customer_trx_id
       and d.application_type                      = 'CASH'
       and d.display                               = 'Y'
       AND (d.gl_date) between ('{p_start_date}')  AND ('{p_end_date}')
       AND B.invoice_currency_code ='INR'
       UNION ALL
       -- Following Query for Exchange Gain and Loss ================================================= Not Working
       SELECT
       hzca.cust_account_id customer_id  ,
        B.BILL_TO_SITE_USE_ID customer_site_id                                       ,
       hzca.account_number  customer_number                   ,
       a.party_name customer_name                                               ,
       d.gl_date                                                                ,
       b.customer_trx_id                                                        ,
       b.trx_number                                                             ,
       (SELECT interface_line_Attribute1
       FROM ra_customer_Trx_lines_All
       where CUSTOMER_TRX_ID=b.CUSTOMER_TRX_ID
       and org_id=b.org_id
       and rownum=1)reference,
       to_char(b.trx_date,'DD-MM-YYYY') trx_date                                ,
       c.receipt_number                                                         ,
       to_char(c.receipt_date,'DD-MM-yyyy') receipt_date                        ,
       decode(e.amount_dr, null, 'CR','DR')   comments                          ,
       e.code_combination_id                                                    ,
       b.INVOICE_CURRENCY_CODE                                                  ,
       b.exchange_rate                                                          ,
       nvl(e.AMOUNT_DR, e.AMOUNT_CR)     amount                                 ,
       nvl(e.ACCTD_AMOUNT_DR,e.ACCTD_AMOUNT_CR)     acctd_amount                ,
       e.source_type                                                            ,
       xxcns_deb_led_get_narration(e.source_type,NULL,B.CUSTOMER_TRX_ID)naration,
       0 customer_trx_id                                                        ,
       0 customer_trx_line_id                                                   ,
       b.ROWID
       FROM
       hz_parties a, hz_cust_accounts hzca ,
       ra_customer_trx_all                                                     b,
       ar_cash_receipts_all                                                    c,
       ar_receivable_applications_all                                          d,
       ar_distributions_all                                                    e
       WHERE a.party_id = hzca.party_id
       AND hzca.cust_account_id                    =  b.BILL_TO_CUSTOMER_ID
       AND b.customer_trx_id                       =  d.APPLIED_CUSTOMER_TRX_ID
       AND c.cash_receipt_id                       =  d.cash_receipt_id
       AND e.SOURCE_ID                             =  d.receivable_application_id
       AND b.org_id                                = '{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(b.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(b.BILL_TO_SITE_USE_ID,'99999999999999'))
       AND e.source_Type                           IN ('EXCH_LOSS', 'EXCH_GAIN')
       AND (d.gl_date) BETWEEN ('{p_start_date}')  AND ('{p_end_date}')
       AND B.invoice_currency_code ='INR'
       UNION ALL
       -- Following Query for Exchange Gain and Loss for CM applied to the invoice ================================================= Not Working
       SELECT
       hzca.cust_account_id customer_id ,
        B.BILL_TO_SITE_USE_ID customer_site_id                                        ,
       hzca.account_number  customer_number                   ,
       a.party_name customer_name                                               ,
       d.gl_date                                                                ,
       b.customer_trx_id                                                        ,
       b.trx_number                                                             ,
       (SELECT interface_line_Attribute1
       FROM ra_customer_Trx_lines_All
       where CUSTOMER_TRX_ID=b.CUSTOMER_TRX_ID
       and org_id=b.org_id
       and rownum=1)reference,
       to_char(b.trx_date,'DD-MM-YYYY') trx_date                                ,
       null                                                         ,
       null                      ,
       decode(e.amount_dr, null, 'CR','DR')   comments                          ,
       e.code_combination_id                                                    ,
       b.INVOICE_CURRENCY_CODE                                                  ,
       b.exchange_rate                                                          ,
       nvl(e.AMOUNT_DR, e.AMOUNT_CR)     amount                                 ,
       nvl(e.ACCTD_AMOUNT_DR,e.ACCTD_AMOUNT_CR)     acctd_amount                ,
       e.source_type                                                            ,
       xxcns_deb_led_get_narration(e.source_type,NULL,B.CUSTOMER_TRX_ID)naration,
       0 customer_trx_id                                                        ,
       0 customer_trx_line_id                                                   ,
       b.ROWID
       FROM
       hz_parties a, hz_cust_accounts hzca ,
       ra_customer_trx_all                                                     b,
       ar_payment_schedules_all                                               c,
       ar_receivable_applications_all                                          d,
       ar_distributions_all                                                    e
       WHERE a.party_id = hzca.party_id
       AND hzca.cust_account_id                    =  b.BILL_TO_CUSTOMER_ID
       AND b.customer_trx_id                       =  d.APPLIED_CUSTOMER_TRX_ID
       AND c.payment_schedule_id                       =  d.payment_schedule_id
       and c.class='CM'
       AND e.SOURCE_ID                             =  d.receivable_application_id
       AND b.org_id                                =   '{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(b.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(b.BILL_TO_SITE_USE_ID,'99999999999999'))
       AND e.source_Type                           IN ('EXCH_LOSS', 'EXCH_GAIN')
       AND (d.gl_date) BETWEEN ('{p_start_date}')  AND ('{p_end_date}')
       AND B.invoice_currency_code ='INR')
       ORDER BY trx_date