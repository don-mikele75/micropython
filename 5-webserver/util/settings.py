import json

class Settings:

    file_name = 'settings.json'
    test_value = 'mikele'

    @staticmethod
    def getDefault():
        s = Settings()
        s.test_value = 'mikele'
        return s

    def save(self):
        settings_json = json.dumps(self.__dict__)
        try:
            f = open(Settings.file_name,'w')
            f.write(settings_json)
            f.close()
            return True
        except:
            return False
        
    @staticmethod
    def load():
        try:
            f = open(Settings.file_name,'r')
            settings_string=f.read()
            f.close()
            settings_dict = json.loads(settings_string)
            result = Settings.getDefault()
            for setting in settings_dict:
                setattr(result,setting, settings_dict[setting])
            return result
        except:
            return Settings.getDefault()