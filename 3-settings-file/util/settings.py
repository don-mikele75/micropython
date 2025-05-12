import json

class Settings:

    file_name = 'settings.json'
    ldr_polling_ms = 0
    led_on_minimum_ldr = 0
    led_on_timeout_sec = 0

    @staticmethod
    def getDefault():
        s = Settings()
        s.ldr_polling_ms = 100
        s.led_on_minimum_ldr = 0
        s.led_on_timeout_sec = 5
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