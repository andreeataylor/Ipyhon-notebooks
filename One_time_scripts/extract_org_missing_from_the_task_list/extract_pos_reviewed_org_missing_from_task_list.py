import pandas as pd
from pandas.io import sql

from utils.loadConfig import load_config
from utils.postgresUtils import get_db_connection_from_config


def load_db_conn_from_config_file(config_file, db_name):
    db_config = load_config(config_file, config_name=db_name)
    db_conn = get_db_connection_from_config(db_config)

    return db_conn


def get_reviewed_organizations_missing_from_the_task_list(start_time, end_time, risk_conn):

    sql_fetch_org = """
    SELECT DISTINCT affected_id as organization_uuid, task_group
    FROM review
    WHERE created BETWEEN '{start_time}'::TIMESTAMP and '{end_time}'::TIMESTAMP
    AND hit = TRUE
    EXCEPT
    SELECT DISTINCT affected_id, task_group
    FROM review_task
    WHERE created BETWEEN '{start_time}'::TIMESTAMP and '{end_time}'::TIMESTAMP
    """.format(start_time=start_time, end_time=end_time)

    return sql.read_sql(sql_fetch_org, risk_conn)


def get_org_info(org_uuids_list, sun_conn):

    sql_fetch_info_org = """
    SELECT o.id as organization_id,
           o.uuid as organization_uuid,
           o.country_id,
           oc.customer_status_id
    FROM organization o
    INNER JOIN organization_customer oc ON oc.organization_id = o.id
    WHERE uuid in ('{organization_uuids}')
    """.format(organization_uuids="','".join([str(uuid) for uuid in set(org_uuids_list)]))

    missing_org = sql.read_sql(sql_fetch_info_org, sun_conn)

    customer_status_mapping = {
        0: 'ACCEPTED',
        1: 'BANNED',
        2: 'UNCONFIRMED_IDENTITY',
        3: 'FROZEN',
        4: 'STOPPED_TRANSACTIONS',
        5: 'DELETED',
        6: 'STOPPED_DEPOSITS'
    }
    missing_org['customer_status'] = missing_org['customer_status_id'].map(lambda x: customer_status_mapping[x])

    return missing_org[['organization_id', 'organization_uuid', 'country_id', 'customer_status']]


def main():

    config_file = "db-config.yaml"
    risk_conn = load_db_conn_from_config_file(config_file, 'risk-write')
    sun_conn = load_db_conn_from_config_file(config_file, 'risk-cloud-slave')

    start_time = '2015-06-01'
    end_time = '2015-07-01'
    country_id_list = ['BR']

    missing_org = get_reviewed_organizations_missing_from_the_task_list(start_time, end_time, risk_conn)
    missing_org_info = get_org_info(missing_org['organization_uuid'].tolist(), sun_conn)
    missing_org = pd.merge(missing_org, missing_org_info, how='inner', on='organization_uuid')

    missing_org_for_list_of_countries = missing_org[missing_org['country_id'].isin(country_id_list)]

    missing_org_for_list_of_countries.to_csv('Missing_org_from_task_list_for_'+str(country_id_list)+'_'+start_time+'_'+
                                             end_time+'.txt', sep='\t', encoding='utf-8', index=False)


if __name__ == '__main__':
    main()
