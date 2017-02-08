import ConfigParser


def read_config(file, param):
    config = ConfigParser.ConfigParser()
    config.read(file)
    param = config.get('Scanner', param)
    return param
