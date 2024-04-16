from configparser import ConfigParser

if __name__ == '__main__':
    config: ConfigParser = ConfigParser(allow_no_value=True)
    config.optionxform = str
    config.read('./configuration.ini')
    parsedConfig: dict = config._sections
    print(parsedConfig)