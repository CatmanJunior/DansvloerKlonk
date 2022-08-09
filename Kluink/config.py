import configparser

config = configparser.ConfigParser()
# print(config.sections())

class Config():
    @classmethod
    def load_config(cls, unique_sections=[]):
        config.read('config.ini')
        for section in config:
            for option in config[section]:
                if section in unique_sections:
                    var_name = option
                else:
                    var_name = section + "_" + option
                setattr(cls, var_name, config[section][option])
        print(dir(Config))

    @classmethod
    def save_config(cls):
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
