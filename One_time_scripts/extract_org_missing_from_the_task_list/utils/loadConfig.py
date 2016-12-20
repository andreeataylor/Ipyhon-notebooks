import yaml


def load_config(filename, config_name='development'):
    """Load database configuration from YAML file and extract a named configuration

    @param filename: The filename (and path) to load
    @param config_name: The name of the configuration to fetch
    @return: A configuration dictionary for use with postgresUtils.get_db_connection_from_config()
    """
    with open(filename) as config_file:
        config = yaml.safe_load(config_file)
        return config[config_name]
