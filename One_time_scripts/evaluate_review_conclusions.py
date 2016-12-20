from pandas.io import sql
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

from true_outcome.evaluate_fraud_decisions_with_true_outcome import evaluate_fraud_decisions
from adhoc_analysis.db import load_config, postgres_utils


def get_reviews(start_period, end_period, risk_conn):
    """
    Fetch the affected id, the review time and the reviewer id from the review table for the given period.
    """
    sql_fetch_review_data = """
    SELECT affected_id,
           created as evaluation_time,
           reviewer as reviewer_id
	FROM review
    WHERE task_group = 'FRAUD'
      AND created >= '{start_period}'::TIMESTAMP
      AND created < '{end_period}'::TIMESTAMP
    """.format(start_period=start_period, end_period=end_period)

    reviews = sql.read_sql(sql_fetch_review_data, risk_conn, parse_dates={'evaluation_time': {'utc': True}})
    reviews['reviewer_id'] = reviews['reviewer_id'].convert_objects(convert_numeric=True)
    print(reviews)
    return reviews


def get_reviewer_names(reviewer_ids_list, sun_conn):
    """
    Fetch the reviewer names for the list of reviewer ids.
    """
    sql_fetch_reviewer_name = """
        SELECT first_name  || ' ' || last_name as reviewer, id as reviewer_id
          FROM izettle.user
        WHERE id in ('{rev_ids}')
    """.format(rev_ids="','".join([str(id) for id in set(reviewer_ids_list)]))

    reviewers = sql.read_sql(sql_fetch_reviewer_name, sun_conn)
    reviewers['reviewer_id'] = reviewers['reviewer_id'].convert_objects(convert_numeric=True)
    return reviewers


def evaluate_fraud_review_conclusions(decisional_entity, start_period, end_period, analysis_time, time_of_outcome,
                                      config_file):
    """
    Parameters
    ----------
    : start_period: a date or a string convertible to date
    : end_period:  a date or a string convertible to date
    : risk_conn: connection to risk database
    : sun_conn: connection to sun database

    Returns a data frame containing
    -------------------------------
    : affected_id - the organization uuid of the merchant
    : review_time - timestamp, the time of the decision
    : rev_id - the user id of the reviewer
    : reviewer - the name of the reviewer
    """
    risk_conn = postgres_utils.get_db_connection_from_config(
        load_config.load_config(config_file, config_name='risk-write'))
    sun_conn = postgres_utils.get_db_connection_from_config(
        load_config.load_config(config_file, 'risk-cloud-slave'))

    if start_period > end_period:
        raise Exception('The start_period must not exceed end_period.')

    reviews = get_reviews(start_period, end_period, risk_conn)
    reviewer_names = get_reviewer_names(reviews['reviewer_id'].tolist(), sun_conn)
    reviews_and_reviewer = pd.merge(reviews, reviewer_names, how='inner', on='reviewer_id')

    evaluations = evaluate_fraud_decisions(affected_id_and_evaluation_time=
                                           reviews_and_reviewer[['affected_id', 'evaluation_time']],
                                           decisional_entity=decisional_entity, analysis_time=analysis_time,
                                           time_of_outcome=time_of_outcome, config_file=config_file)

    reviews_and_reviewer = reviews_and_reviewer[['reviewer', 'evaluation_time', 'affected_id']]
    evaluated_reviews = pd.merge(reviews_and_reviewer, evaluations, how='inner', on=['affected_id', 'evaluation_time'])
    evaluated_reviews.to_csv('Reviews_evaluation_' + str(start_period) + '_to_' + str(end_period) + '.tsv', sep='\t',
                             encoding='utf-8', index=False)


if __name__=="__main__":
    end_period = datetime.datetime.now() - relativedelta(months=4)
    start_period = end_period - relativedelta(months=1)

    print(start_period, end_period)

    from datetime import datetime
    analysis_time = datetime.utcnow()
    decisional_entity = 'review'
    time_of_outcome = 'at_evaluation_time'
    config_file = '../adhoc_analysis/db/db-config.yaml'


    evaluate_fraud_review_conclusions(decisional_entity, start_period, end_period, analysis_time, time_of_outcome,
                                      config_file)