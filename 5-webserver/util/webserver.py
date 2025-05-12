import uasyncio as asyncio
import re
from lib.microdot import Microdot
from util.settings import Settings

class Webserver:

    settings: Settings
    app = Microdot
    config_changed_listeners: list
    log_async: function

    def __init__(self):
        global app
        self.settings = Settings.load()
        app = Microdot()
        self.config_changed_listeners = list()
        
        @app.route('/')
        async def index(request):
            return self.create_html(), 200, {'Content-Type': 'text/html'}

        @app.route('/save')
        async def save(request):
            self.settings.test_value = re.search('(?:test_value=)(.*)(?:&|$)', request.query_string).group(1) # type: ignore
            self.settings.save()
            for func in self.config_changed_listeners:
                await func()
            return await index(request)

    def add_config_changed_listener(self, func):
        self.config_changed_listeners.append(func)

    def create_html(self):
        file = open('default.html','r')
        html = file.read()
        file.close()

        input = '''
        <form action="save"> 
            <label for="test_value">test_value:</label><br>
            <input type="text" id="test_value" name="test_value" value="{0}"><br>
            <input type="submit" value="Submit">
        </form>'''
        return html.format(
            input.format(
                self.settings.test_value))

    async def run_watchdog(self):
        print('Webserver daemon started...')
        app.run(debug=True)