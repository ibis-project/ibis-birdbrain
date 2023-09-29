# imports
import toml


# functions
def read_config(config_file: str = "config.toml", config_section: str | None = None):
    """Reads the config file and returns the config section"""
    try:
        config = toml.load(config_file)
    except FileNotFoundError:
        print(f"Config file {config_file} not found!")
        config = {}
    if config_section is None:
        return config
    else:
        try:
            return config[config_section]
        except KeyError:
            print(f"Config section {config_section} not found!")
            if config_section == "system":
                config[config_section] = {"backend_uri": "duckdb://birdbrain.ddb"}
                return config[config_section]
            elif config_section == "eda":
                config[config_section] = {"backend_uri": "duckdb://"}
                return config[config_section]
            exit(1)
