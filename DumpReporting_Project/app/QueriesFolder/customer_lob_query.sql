select DISTINCT
    ac.customer_number ,ac.customer_name ,
    hcas.cust_account_id customer_id,SEGMENT4 BRANCH
    from hz_cust_acct_Sites_All hcas,ra_territories rt,ar_customers ac
    where hcas.TERRITORY_ID=rt.TERRITORY_ID
    and ac.customer_id= hcas.cust_account_id
    and (customer_name LIKE '%{party_name}%' OR customer_name LIKE '%{code}%')
    and SEGMENT4 LIKE 'Delhi%'