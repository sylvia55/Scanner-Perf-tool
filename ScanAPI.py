import Tool
import ConfigParser

def main():

    config = ConfigParser.ConfigParser()
    config.read('bin\API.config')
    param = config.get('Scanner', 'url')
    #url = Tool.read_config(,'url')
    print param

if __name__ == '__main__':
    main()