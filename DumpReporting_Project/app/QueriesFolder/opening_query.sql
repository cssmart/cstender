SELECT ----SUM (amount) tran_open_bal_cr,
                   SUM (amount_other_currency) func_open_bal_cr
            ---into v_tran_tot_amt,v_func_tot_amt

            FROM   (SELECT   hzca.cust_account_id customer_id,
                 hzca.account_number /*a.party_number*/ customer_number,
                 a.party_name customer_name, d.gl_date, b.customer_trx_id,
                 b.trx_number, TO_CHAR (b.trx_date, 'DD-MM-YYYY') trx_date,
                 NULL receipt_number, NULL receipt_date,
                 SUBSTR (b.comments, 1, 50) remarks,
                 d.code_combination_id account_id,
                 b.invoice_currency_code currency_code, b.exchange_rate,
                 d.amount amount,
                 (d.amount * NVL (b.exchange_rate, 1)
                 ) amount_other_currency, f.TYPE, b.customer_trx_id,
                 d.customer_trx_line_id, b.ROWID
            FROM hz_parties a,
                 hz_cust_accounts hzca,
                 ra_customer_trx_all b,
                 ra_cust_trx_line_gl_dist_all d,
                 gl_code_combinations e,
                 ra_cust_trx_types_all f,
                 ar_payment_schedules_all g
           WHERE a.party_id = hzca.party_id
             AND b.bill_to_customer_id = hzca.cust_account_id
             AND b.complete_flag = 'Y'
             AND d.customer_trx_id = b.customer_trx_id
             AND d.account_class = 'REC'
             AND e.code_combination_id = d.code_combination_id
             AND f.cust_trx_type_id = b.cust_trx_type_id
             AND f.TYPE IN ('INV', 'CM', 'DM', 'DEP')
             AND d.latest_rec_flag = 'Y'
             AND g.customer_trx_id = b.customer_trx_id
             AND b.org_id = '{p_org_id}'
             AND TO_DATE (g.gl_date) <  ('{p_start_date}')
          --and b.bill_to_site_use_id=:customer_site_id
             AND g.payment_schedule_id IN (
                                     SELECT MIN (payment_schedule_id)
                                       FROM ar_payment_schedules_all
                                      WHERE customer_trx_id =
                                                             g.customer_trx_id)
        UNION ALL
-- Following Query for Cash receipts
        SELECT   hzca.cust_account_id customer_id,
                 hzca.account_number /*a.party_number*/ customer_number,
                 a.party_name customer_name, e.gl_date, 0, NULL, NULL,
                 b.receipt_number, TO_CHAR (b.receipt_date, 'DD-MM-YYYY'),
                 NULL, d.cash_ccid account_id, b.currency_code,
                 b.exchange_rate, b.amount * -1 amount,
                 (b.amount * -1 * NVL (b.exchange_rate, 1)
                 ) amount_other_currency,
                 'REC' TYPE, 0, 0, b.ROWID
            FROM hz_parties a,
                 hz_cust_accounts hzca,
                 ar_cash_receipts_all b,
                 gl_code_combinations c,
                 ar_receipt_method_accounts_all d,
                 ar_cash_receipt_history_all e,
                 ar_payment_schedules_all f
           WHERE a.party_id = hzca.party_id
             AND b.pay_from_customer = hzca.cust_account_id
             AND b.remit_bank_acct_use_id = d.remit_bank_acct_use_id
             AND d.receipt_method_id = b.receipt_method_id
             AND d.cash_ccid = c.code_combination_id
             AND e.cash_receipt_id = b.cash_receipt_id
           --and NVL(b.customer_site_use_id,-1)=:customer_site_id
             AND e.cash_receipt_history_id IN (
                    SELECT MIN (incrh.cash_receipt_history_id)
                      FROM ar_cash_receipt_history_all incrh
                     WHERE incrh.cash_receipt_id = b.cash_receipt_id
                       AND incrh.status <> 'REVERSED')
             AND f.cash_receipt_id = b.cash_receipt_id
             AND b.org_id = '{p_org_id}'
             AND (e.gl_date) <  ('{p_start_date}')
        UNION ALL
-- Following Query for Receipt WriteOff
        SELECT   hzca.cust_account_id customer_id,
                 hzca.account_number /*a.party_number*/ customer_number,
                 a.party_name customer_name, g.gl_date, 0, NULL, NULL,
                 b.receipt_number, TO_CHAR (b.receipt_date, 'DD-MM-YYYY'),
                 NULL, d.cash_ccid account_id, b.currency_code,
                 b.exchange_rate, g.amount_applied amount,
                 (g.amount_applied * NVL (b.exchange_rate, 1)
                 ) amount_other_currency,
                 'W/O' TYPE, 0, 0, b.ROWID
            FROM hz_parties a,
                 hz_cust_accounts hzca,
                 ar_cash_receipts_all b,
                 gl_code_combinations c,
                 ar_receipt_method_accounts_all d,
                 ar_cash_receipt_history_all e,
                 ar_payment_schedules_all f,
                 ar_receivable_applications_all g
           WHERE a.party_id = hzca.party_id
             AND b.pay_from_customer = hzca.cust_account_id
             AND g.applied_payment_schedule_id = -3
             AND g.cash_receipt_id = b.cash_receipt_id
             AND g.cash_receipt_history_id = e.cash_receipt_history_id
             AND g.status = 'ACTIVITY'
             AND b.remit_bank_acct_use_id = d.remit_bank_acct_use_id
             AND d.receipt_method_id = b.receipt_method_id
             AND d.cash_ccid = c.code_combination_id
             AND e.cash_receipt_id = b.cash_receipt_id
             AND f.cash_receipt_id = b.cash_receipt_id
             AND b.org_id = '{p_org_id}'
          ---and NVL(b.customer_site_use_id,-1)=:customer_site_id
             AND  (g.gl_date) <  ('{p_start_date}')
             AND NOT EXISTS (
                    SELECT 1
                      FROM ar_cash_receipt_history_all
                     WHERE cash_receipt_id = b.cash_receipt_id
                       AND status = 'REVERSED')
        UNION ALL
-- Following Query for Receipt Reversal
        SELECT   hzca.cust_account_id customer_id,
                 hzca.account_number /*a.party_number*/ customer_number,
                 a.party_name customer_name, e.gl_date gl_date, 0, NULL,
                 TO_CHAR (e.trx_date, 'DD-MM-YYYY') trx_date,
                 b.receipt_number, TO_CHAR (b.receipt_date, 'DD-MM-YYYY'),
                 NULL, c.code_combination_id account_id, b.currency_code,
                 b.exchange_rate, b.amount amount,
                 (b.amount * NVL (b.exchange_rate, 1)
                 ) amount_other_currency, 'REV' TYPE, 0, 0, b.ROWID
            FROM hz_parties a,
                 hz_cust_accounts hzca,
                 ar_cash_receipts_all b,
                 gl_code_combinations c,
                 ar_receipt_method_accounts_all d,
                 ar_cash_receipt_history_all e,
                 ar_payment_schedules_all f
           WHERE a.party_id = hzca.party_id
             AND b.pay_from_customer = hzca.cust_account_id
             AND b.remit_bank_acct_use_id = d.remit_bank_acct_use_id
             AND d.receipt_method_id = b.receipt_method_id
             AND d.cash_ccid = c.code_combination_id
             AND e.cash_receipt_id = b.cash_receipt_id
             AND f.cash_receipt_id = b.cash_receipt_id
             AND b.org_id = '{p_org_id}'
             AND e.status = 'REVERSED'
          --and NVL(b.customer_site_use_id,-1)=:customer_site_id
             AND  (e.gl_date) < ('{p_start_date}')
             AND b.reversal_date IS NOT NULL
        UNION ALL
-- Following Query for Adjustments
        SELECT   hzca.cust_account_id customer_id,
                 hzca.account_number /*A.PARTY_NUMBER*/ customer_number,
                 a.party_name customer_name, b.gl_date, 0,
                 b.adjustment_number,
                 TO_CHAR (b.apply_date, 'DD-MM-YYYY') trx_date,
                 NULL receipt_number, NULL receipt_date,
                 SUBSTR (b.comments, 1, 50) remarks,
                 b.code_combination_id account_id,
                 c.invoice_currency_code currency_code, c.exchange_rate,
                 b.amount amount,
                 (b.amount * NVL (c.exchange_rate, 1)
                 ) amount_other_currency, 'ADJ' TYPE, 0, 0, b.ROWID
            FROM hz_parties a,
                 hz_cust_accounts hzca,
                 ar_adjustments_all b,
                 ra_customer_trx_all c,
                 ar_payment_schedules_all d,
                 gl_code_combinations e
           WHERE b.customer_trx_id = c.customer_trx_id
             AND b.customer_trx_id NOT IN (
                    SELECT customer_trx_id
                      FROM ar_adjustments_all
                     WHERE chargeback_customer_trx_id IS NOT NULL
                        OR created_from = 'REVERSE_CHARGEBACK')
                                         /*added by abezgam for bug#10228717*/
             AND a.party_id = hzca.party_id
             AND c.bill_to_customer_id = hzca.cust_account_id
             AND b.status = 'A'
             AND e.code_combination_id = b.code_combination_id
             AND b.payment_schedule_id = d.payment_schedule_id
             AND b.customer_trx_id = d.customer_trx_id
             AND c.org_id = '{p_org_id}'
           --and c.bill_to_site_use_id=:customer_site_id
             AND  (b.gl_date) < ('{p_start_date}')
        UNION ALL
-- -- Following Query for Discounts
        SELECT   hzca.cust_account_id customer_id,
                 hzca.account_number /*a.party_number*/ customer_number,
                 a.party_name customer_name, d.gl_date, b.customer_trx_id,
                 b.trx_number, TO_CHAR (b.trx_date, 'DD-MM-YYYY') trx_date,
                 NULL receipt_number, NULL receipt_date,
                 SUBSTR (b.comments, 1, 50) remarks,
                 earned_discount_ccid account_id,
                 b.invoice_currency_code currency_code, b.exchange_rate,
                 d.earned_discount_taken * -1 amount,
                 d.acctd_earned_discount_taken * -1 amount_other_currency,
                 'DSC' TYPE, b.customer_trx_id, 0, b.ROWID
            FROM hz_parties a,
                 hz_cust_accounts hzca,
                 ra_customer_trx_all b,
                 ar_receivable_applications_all d
           WHERE a.party_id = hzca.party_id
             AND b.bill_to_customer_id = hzca.cust_account_id
             AND b.complete_flag = 'Y'
             AND d.earned_discount_taken IS NOT NULL
             AND d.earned_discount_taken <> 0
             AND b.org_id = '{p_org_id}'
             AND b.customer_trx_id = d.applied_customer_trx_id
             AND d.application_type = 'CASH'
             AND d.display = 'Y'
           --and NVL(b.bill_to_site_use_id,-1)=:customer_site_id
             AND  (d.gl_date) <  ('{p_start_date}')
        UNION ALL
-- Following Query for Exchange Gain and Loss
        SELECT   hzca.cust_account_id customer_id,
                 hzca.account_number /*a.party_number*/ customer_number,
                 a.party_name customer_name, d.gl_date, b.customer_trx_id,
                 b.trx_number, TO_CHAR (b.trx_date, 'DD-MM-YYYY') trx_date,
                 c.receipt_number,
                 TO_CHAR (c.receipt_date, 'DD-MM-yyyy') receipt_date,
                 DECODE (e.amount_dr, NULL, 'CR', 'DR') comments,
                 e.code_combination_id, b.invoice_currency_code,
                 b.exchange_rate, NVL (e.amount_dr * -1, e.amount_cr) amount,
                 NVL (e.acctd_amount_dr * -1, e.acctd_amount_cr) acctd_amount,
                 e.source_type, 0 customer_trx_id, 0 customer_trx_line_id,
                 b.ROWID
            FROM hz_parties a,
                 hz_cust_accounts hzca,
                 ra_customer_trx_all b,
                 ar_cash_receipts_all c,
                 ar_receivable_applications_all d,
                 ar_distributions_all e
           WHERE a.party_id = hzca.party_id
             AND hzca.cust_account_id = b.bill_to_customer_id
             AND b.customer_trx_id = d.applied_customer_trx_id
             AND c.cash_receipt_id = d.cash_receipt_id
             AND e.source_id = d.receivable_application_id
             AND b.org_id = '{p_org_id}'
             AND e.source_type IN ('EXCH_LOSS', 'EXCH_GAIN')
         ---and NVL(b.bill_to_site_use_id,-1)=:customer_site_id
             AND (d.gl_date) < ('{p_start_date}')
        UNION ALL
-- Following Query for Exchange Gain and Loss for CM applied to the invoice
        SELECT   hzca.cust_account_id customer_id,
                 hzca.account_number customer_number,
                 a.party_name customer_name, d.gl_date, b.customer_trx_id,
                 b.trx_number, TO_CHAR (b.trx_date, 'DD-MM-YYYY') trx_date,
                 NULL, NULL, DECODE (e.amount_dr, NULL, 'CR', 'DR') comments,
                 e.code_combination_id, b.invoice_currency_code,
                 b.exchange_rate, NVL (e.amount_dr * -1, e.amount_cr) amount,
                 NVL (e.acctd_amount_dr * -1, e.acctd_amount_cr) acctd_amount,
                 e.source_type, 0 customer_trx_id, 0 customer_trx_line_id,
                 b.ROWID
            FROM hz_parties a,
                 hz_cust_accounts hzca,
                 ra_customer_trx_all b,
                 ar_payment_schedules_all c,
                 ar_receivable_applications_all d,
                 ar_distributions_all e
           WHERE a.party_id = hzca.party_id
             AND hzca.cust_account_id = b.bill_to_customer_id
             AND b.customer_trx_id = d.applied_customer_trx_id
             AND c.payment_schedule_id = d.payment_schedule_id
             AND c.CLASS = 'CM'
             AND e.source_id = d.receivable_application_id
             AND b.org_id = '{p_org_id}'
             AND e.source_type IN ('EXCH_LOSS', 'EXCH_GAIN')
             AND TO_DATE (d.gl_date) <  ('{p_start_date}')
          ---and NVL(b.bill_to_site_use_id,-1)=:customer_site_id
    ) a
 WHERE a.customer_id = '{p_customer_id}'
 AND a.currency_code = '{currency_code}'