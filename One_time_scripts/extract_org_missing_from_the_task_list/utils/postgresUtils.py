from getpass import getpass
from psycopg2 import connect


def get_db_connection_from_config(configuration):
    """Creates a psycopg2 connection object from the provided configuration

    @param configuration: A configuration dictionary containing the required fields
    @return: A connection object
    """

    if not 'password' in configuration:
        password = getpass('Password for ' + configuration['user'] + '@' + configuration['host'] + '\n')
    else:
        password = configuration['password']

    c = connect(host=configuration['host'],
                user=configuration['user'],
                password=password,
                database=configuration['database'],
                port=configuration['port'])
    return c
