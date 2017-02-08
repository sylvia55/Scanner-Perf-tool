import ConfigParser
import os

def test_config():

    config = ConfigParser.ConfigParser()
    config.read('unit\config.ini')
    tag = config.get('cases', 'category')
    print tag
    print 'this is '
    print config.sections()
    a = []
    for section in config.sections():

        try:
            if str(config.get(section, 'tag')) == tag:
                a.append(section)
                print config.get(section, 'tag')
            else:
                print 'else here'
        except Exception, e:
            print e
    return a


# print test_config()

def get_pid():
    print os.getpid()

get_pid()