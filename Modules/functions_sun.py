import pandas as pd
from pandas.io import sql
from Modules.constants import customer_status_mapping, banned_status_mapping

def get_accepted_organization_uuids(sun_conn):

    sql_fetch_accepted_customer = """
    SELECT o.uuid as uuid_sun, o.country_id, oc.customer_status_id
    FROM organization_customer oc
      INNER JOIN organization o ON o.id = oc.organization_id
    WHERE customer_status_id = 0
    """
    return pd.read_sql(sql_fetch_accepted_customer, sun_conn)


def get_organization_customer(sun_conn):
    sql_fetch_accepted_customer = """
    SELECT o.uuid as uuid_sun, o.country_id, oc.*
    FROM organization_customer oc
      INNER JOIN organization o ON o.id = oc.organization_id
    """
    return pd.read_sql(sql_fetch_accepted_customer, sun_conn)


def get_review_tasks(risk_conn):
    sql_fetch_review_tasks = """
    select affected_id, task_group, country_id, created
    from review_task rt
    """
    return pd.read_sql(sql_fetch_review_tasks, risk_conn)


def get_review(risk_conn):
    sql_fetch_review = """
    select *
    from review
    """
    return pd.read_sql(sql_fetch_review, risk_conn)

def get_organization_customer_history(sun_conn):
    sql_fetch_organization_customer_history = """
    SELECT o.uuid as uuid_sun, o.country_id, och.*
    FROM history.organization_customer_history och
    INNER JOIN organization o
      ON o.id = och.organization_id
    """
    return pd.read_sql(sql_fetch_organization_customer_history, sun_conn)


def get_active_banned_status(sun_conn):
    sql_fetch_status = """
    SELECT organization_id
      , bs.banned_reason_id
      , bs.created as time_of_ban_reason
    FROM banned_status bs
    WHERE bs.is_active
    """
    return pd.read_sql(sql_fetch_status, sun_conn)


def get_mc_category_and_business_type_description(sun_conn):
    sql_fetch_mcc_and_bs_type = """
    SELECT organization_id,
        mc.name_text_key as mc_category,
        btd.name as business_type_description,
        btd.is_active as business_type_is_active,
        btd.id as business_type_id,
        btd.parent_id as business_type_parent,
        o.uuid as uuid_sun
    FROM organization_customer oc
    LEFT JOIN business_type_description btd ON btd.id = oc.business_type_description_id
    LEFT JOIN merchant_category mc ON mc.id = oc.merchant_category_id
    INNER JOIN organization o ON o.id = oc.organization_id
    """
    return pd.read_sql(sql_fetch_mcc_and_bs_type, sun_conn)


def get_payments_last_month_from_UK(sun_conn):
    sql_fetch_active_mc = """
    SELECT
      receiver_organization_id AS organization_id,
      transaction_timestamp,
      amount/100::float AS amount_nf,
      commission_amount/100::float AS revenue,
      uuid as card_payment_uuid
    FROM card_payment
    WHERE currency_id = 'GBP'
      AND transaction_timestamp between NOW() and NOW() - INTERVAL '1 MONTH'
    """
    return pd.read_sql(sql_fetch_active_mc, sun_conn)


def get_banned_statuses_history(sun_conn):
    sql_fetch_corganization_customer_history = """
    SELECT organization_id
      , bs.banned_reason_id
      , bs.created as time_of_ban_reason
      , bs.is_active
    FROM banned_status bs
    """
    return pd.read_sql(sql_fetch_corganization_customer_history, sun_conn)


def get_banned_statuses_for_organizations_currently_banned(sun_conn):
    """
    Fetch the active ban statuses for the merchants that are currently banned. Out of the organizations with active ban
    statuses are filtered out the organizations that are not banned any more. This filtering is needed because when
    customer status is changed from BANNED to a different one, the banned_status table is not updated and last status
    remains active.
    """
    sql_fetch_active_banned_status = """
    SELECT o.uuid as uuid_sun, bs.organization_id, banned_reason_id, bs.created, o.country_id
    FROM banned_status bs
      INNER JOIN organization o
        ON o.id = bs.organization_id
    WHERE is_active
    """

    sql_fetch_banned_organizations = """
    SELECT oc.organization_id
    FROM organization_customer oc
    WHERE oc.customer_status_id = 1
    """

    active_banned_statuses = pd.read_sql(sql_fetch_active_banned_status, sun_conn)
    list_currently_banned_organizations = pd.read_sql(sql_fetch_banned_organizations, sun_conn)['organization_id'].\
        tolist()

    return active_banned_statuses[active_banned_statuses.organization_id.isin(list_currently_banned_organizations)]


def get_tag_entity(sun_conn):
    sql_fetch_tags = """
    select te.tag_id, o.uuid as uuid_sun, et.name as entity_type_name, te.is_active as tag_is_active,
      te.created as created_time, te.created_by as tag_created_by, te.updated as updated_time,
      te.updated_by as te_updated_by, te.entity_id as organization_id
    from tag_entity te
    inner join entity_type et on et.id = te.entity_type_id
    inner join organization o on o.id = te.entity_id
    """
    return pd.read_sql(sql_fetch_tags, sun_conn)


def get_tag_table(sun_conn):
    return pd.read_sql("""select * from tag""", sun_conn)


def get_current_statuses_including_ban_reason(sun_conn):
    sql_fetch_curent_statuses = """
    select oc.organization_id, oc.legal_entity_type_id, oc.customer_status_id, oc.contact_email, oc.legal_entity_nr, oc.contact_name,
      bs.banned_reason_id, bs.created as ban_created, o.uuid as uuid_sun, o.country_id, oc.legal_city, o.created as 
      registration_timestamp, ccg.name as limits_group, oc.commission_model_id
    from organization_customer oc
    inner join organization o on o.id = oc.organization_id
    left join (select * from  banned_status where is_active) bs
      on bs.organization_id = oc.organization_id
    inner join customer_config_group ccg on ccg.id = oc.customer_config_group_id
    """
    current_statuses = pd.read_sql(sql_fetch_curent_statuses, sun_conn)
    current_statuses['customer_status'] = current_statuses['customer_status_id'].map(lambda x: customer_status_mapping[x])
    current_statuses['ban_reason'] = current_statuses['banned_reason_id'].map(lambda x: banned_status_mapping[x] if not pd.isnull(x) else x)
    current_statuses['complete_customer_status'] = current_statuses.apply(
        lambda row: row['customer_status'] + '_' + row['ban_reason'] 
        if not pd.isnull(row['ban_reason']) and row['customer_status'] == 'BANNED' else row['customer_status'], axis=1) 
    return current_statuses


def get_commission_config(sun_conn):
    sql_fetch_commission_config = """
    select 
       organization_id, 
       o.uuid as uuid_sun, 
       ccg.name as commission_group_name, 
       ccg.description as commission_group_description
    from commission_config_group_organization ccgo
    inner join commission_config_group ccg on ccg.id = ccgo.group_id
    inner join organization o on o.id = ccgo.organization_id
    """
    return pd.read_sql(sql_fetch_commission_config, sun_conn)


def get_shipped_reader_orders(sun_conn):
    sql_fetch_shipped_reader_orders = """
    select ro.country_id, ro.organization_id, ro.total_amount, ro.created, ro.contact_name,
      ro.currency_id, count(roc.id)
    from reader_order ro
        inner join reader_order_content roc on roc.reader_order_id = ro.id
    where ro.ready_for_shipment
    group by ro.country_id, ro.organization_id, ro.total_amount, ro.created, ro.contact_name,
      ro.currency_id
    """
    return pd.read_sql(sql_fetch_shipped_reader_orders, sun_conn)


def get_bank_account_table(sun_conn):
    sql_fetch_bank_accounts = """
    select ba.*, o.uuid as uuid_sun 
    from bank_account ba
    inner join organization o on o.id = ba.organization_id
    """
    return pd.read_sql(sql_fetch_bank_accounts, sun_conn)


def get_bad_merchants(risk_conn):
    sql_fetch_bad_merchants = """
    select *
    from bad_merchant
    """
    return pd.read_sql(sql_fetch_bad_merchants, risk_conn)


def get_edge_table(risk_conn):
    sql_fetch_edge_table = """
    select *
    from edge
    """
    return pd.read_sql(sql_fetch_edge_table, risk_conn)


def get_binpar_table(sun_conn):
    sql_fetch_binpar_table = """
    select bin, card_brand, issuing_bank, card_type, card_category, country_name, country_id
    from binpar
    """
    return pd.read_sql(sql_fetch_binpar_table, sun_conn)


def get_gurrent_balance_in_each_account(organization_id, sun_conn):
    d = {'organization_id': organization_id}
    sql_fetch_account_transaction = """
    WITH accounts as (
      SELECT
        a.id as account_id,
        at.id as account_type_id,
        max(at.name) as account_type
      FROM account a
      INNER JOIN account_type at on a.account_type_id = at.id
      WHERE organization_id = {'organization_id'}
      AND account_type_id IN (2,3,6,7,10,12,17,18)
      GROUP BY a.id, at.id
    )
    SELECT
      SUM(amount) AS amount,
      account_type_id,
      max(account_type)
    FROM (
        SELECT
          SUM(amount) AS amount,
          a.account_type_id,
          max(a.account_type) as account_type
        FROM stats.account_transaction_agg_month satm
        INNER JOIN accounts a ON satm.account_id = a.account_id
        WHERE satm.timestamp_month < date_trunc('month', now())
        GROUP BY a.account_type_id
      UNION ALL
        SELECT
          SUM(amount) AS amount,
          a.account_type_id,
          max(a.account_type) as account_type
        FROM stats.account_transaction_agg_day satd
        INNER JOIN accounts a ON satd.account_id = a.account_id
        WHERE satd.timestamp_day BETWEEN date_trunc('month', now()) AND date_trunc('day', now() - interval '1 day')
        GROUP BY a.account_type_id
      UNION ALL
        SELECT
          SUM(amount) AS amount,
          a.account_type_id,
          max(a.account_type) as account_type
        FROM stats.account_transaction_agg_hour sath
        INNER JOIN accounts a ON sath.account_id = a.account_id
        WHERE sath.timestamp_hour BETWEEN date_trunc('day', now()) AND date_trunc('hour', now() - interval '1 hour')
        GROUP BY a.account_type_id
      UNION ALL
        SELECT
          SUM(amount_fractionized) AS amount,
          a.account_type_id,
          max(a.account_type) as account_type
       FROM account_transaction at
        INNER JOIN accounts a ON at.account_id = a.account_id
        WHERE at.timestamp >= date_trunc('hour', now())
        GROUP BY a.account_type_id
    ) AS tmp
    GROUP BY account_type_id
    """.format(**d)
    return pd.read_sql(sql_fetch_account_transaction, sun_conn)


def get_account_transaction_liquid_accounts_agg_day(sun_conn):
    sql_fetch_account_transaction_agg = """
    select *
    from stats.account_transaction_agg_day
    where account_type_id in (10, 2)
    """
    return pd.read_sql(sql_fetch_account_transaction_agg, sun_conn)


def get_account_transaction_liquid_accounts(sun_conn):
    sql_fetch_account_transaction_liquid_accounts = """
    select at.id, at.account_id, at.amount_fractionized, at.timestamp, a.account_type_id, a.organization_id, a.currency_id
      from account_transaction at
      inner join account a on a.id = at.account_id
    where a.account_type_id in (10, 2)
    """
    return pd.read_sql(sql_fetch_account_transaction_liquid_accounts, sun_conn)


def get_cryptogram(risk_conn):
    sql_fetch_cryptogram = """
    select *
    from cryptogram
    """
    return pd.read_sql(sql_fetch_cryptogram, risk_conn)


def get_credit_reports_for_GB_companies(sun_conn):
    sql_fetch_credit_reports_GB = """
    SELECT rcd.id as rcd_id, rcd.company_email, rcd.company_legal_entity_nr, rcd.company_category, rcd.person_legal_entity_nr,
      registration_state_id, rcd.organization_id, ccr.id as ccr_id, ccr.capital, ccr.updated, ccr.service_provider_name, 
      ccr.report_type, ccr.xml
    FROM registration_company_data rcd
      JOIN registration_company_data_company_credit_report rcdccr ON rcd.id = rcdccr.registration_company_data_id
      JOIN company_credit_report ccr ON ccr.id = rcdccr.company_credit_report_id
    WHERE rcd.organization_id IS NOT NULL
      AND rcd.country_id = 'GB'
    ORDER BY rcd.organization_id, ccr.id DESC
    """
    return sql.read_sql(sql_fetch_credit_reports_GB, sun_conn)


def get_registration_data(sun_conn):
    sql_fetch_credit_reports_GB = """
    SELECT rcd.id as rcd_id, company_email, company_legal_entity_nr, company_category, person_legal_entity_nr,
      registration_state_id, rcd.organization_id, personal_guarantor, created, updated, company_type
    FROM registration_company_data rcd
    WHERE rcd.organization_id IS NOT NULL
    """
    return pd.read_sql(sql_fetch_credit_reports_GB, sun_conn)


def get_user_table(sun_conn):
    sql_fetch_user = """
    SELECT *
    FROM izettle.user
    """
    return pd.read_sql(sql_fetch_user, sun_conn)


def get_advance_netting(gdp_analyst_conn):
    sql_fetch_advance_netting = """
    SELECT organization_uuid, cash_advance_uuid, amount, netted, currency_id, type, cash_flow_source
    FROM advance_netting
    """
    return pd.read_sql(sql_fetch_advance_netting, gdp_analyst_conn)


def get_issued_advance(gdp_analyst_conn):
    sql_fetch_issued_advance = """
    SELECT ia.cash_advance_uuid, ia.organization_uuid, ia.country_id, ia.ticket, ia.ticket_eur, ia.fee, fee_eur,
      ia.total_claim, ia.total_claim_eur, ia.current_netting_basis_points, ia.current_status, ia.last_status_update, 
      ia.issued, ia.first_netting, ia.last_netting, ia.sum_netted, ia.sum_netted_eur, ia.total_claim_left_to_net,
      ia.total_claim_left_to_net_eur, ia.flow_type, aobu.payoff_time_days
    FROM issued_advance ia
    LEFT JOIN advance_offer_boundary_used aobu ON aobu.offer_boundary_id = ia.offer_boundary_id
    """
    return pd.read_sql(sql_fetch_issued_advance, gdp_analyst_conn)


def get_purchase_library_product(sun_conn):
    sql_fetch_purchase_product = """
    SELECT id, purchase_id, organization_id, user_id, is_library, name, image_lookup_key, created, unit_price, 
      variant_name, description, unit_name
    FROM purchase_product
    where is_library
    """
    return pd.read_sql(sql_fetch_purchase_product, sun_conn)

def get_purchase_created_library_product(gdp_engineer_conn):
    sql_fetch_purchase_product = """
    SELECT organization_uuid, name, variant_name, image_lookup_key
    FROM event.purchase_created_product
    WHERE is_library_product
        AND sent_at > '2016-01-01 02:52:27.959000'
    """
    return pd.read_sql(sql_fetch_purchase_product, gdp_engineer_conn)


def get_tags_complete(sun_conn):
    sql_fetch_tags = """
    select te.tag_id, o.uuid as organization_uuid, tp.title as parent_title, t.title, t.description, 
        et.name as entity_type_name, te.is_active as tag_is_active, te.created as tag_created, 
        te.created_by as tag_created_by, te.updated as updated_time,  te.updated_by as te_updated_by, 
        te.entity_id as organization_id, tc.comment, tc.created as comment_created
    from tag_entity te
    inner join entity_type et on et.id = te.entity_type_id
    inner join organization o on o.id = te.entity_id
    inner join tag_comment tc on te.id = tc.tag_entity_id
    inner join tag t on t.id = te.tag_id
    inner join tag tp on t.parent_id = tp.id
    """
    return pd.read_sql(sql_fetch_tags, sun_conn)

def get_labels_casey(casey_conn):
    sql_fetch_labels = """
    SELECT lc.name as class_name, l.parent_id AS organization_uuid, created, deleted, created_by_user_id, deleted_by_user_id
    FROM label_class lc
    INNER JOIN label l ON lc.id = l.label_class_id
    """
    return pd.read_sql(sql_fetch_labels, casey_conn)

def get_case_view(casey_conn):
    sql_fetch_cases = """
    SELECT affected_id, category, created, score, subject, description
    FROM case_view
    """
    return pd.read_sql(sql_fetch_cases, casey_conn)

def get_mc_that_changed_bank_account(sun_conn):
    sql_fetch = """
    SELECT o.uuid as uuid_sun, count(DISTINCT (ba.bank_account_number)) AS count_ba_numbers
    FROM bank_account ba
    inner join organization o on o.id=ba.organization_id
    WHERE ba.country_id = 'GB' 
    
       -- AND original_bank_account_number IS NOT NULL
       
    GROUP BY o.uuid
    HAVING count(DISTINCT (ba.bank_account_number)) > 1
    """
    return pd.read_sql(sql_fetch, sun_conn)

def get_acquirer(sun_conn):
    sql_fetch_acquirer = """
    SELECT *
    FROM organization_enrollment_status
    """
    return pd.read_sql(sql_fetch_acquirer, sun_conn)

def get_mortal_kombat_one_year_cpv_prediction(gdp_analyst_conn):
    sql_mortal_kombat = """
    SELECT *
    FROM view._mortal_kombat_v2
    """
    return pd.read_sql(sql_mortal_kombat, gdp_analyst_conn)

def get_portal_logins(gdp_engineer):
    sql_fetch_portal_logins = """
    SELECT organization_uuid, timestamp
    FROM view.portal_login
    WHERE organization_uuid IS NOT NULL
    """
    return pd.read_sql(sql_fetch_portal_logins, gdp_conn)


def get_portal_requests(gdp_engineer):
    sql_fetch_portal_requests = """
    SELECT organization_uuid, subject, timestamp
    FROM view.portal_request
    WHERE organization_uuid IS NOT NULL
    """
    return pd.read_sql(sql_fetch_portal_requests, gdp_conn)

def get_sms_receipts(sun_conn):
    sql_fetch_sms_receipts = """
    select * from purchase
    where sms_receipt_owner_id is not null
    """
    return pd.read_sql(sql_fetch_sms_receipts, sun_conn)