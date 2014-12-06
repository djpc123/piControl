import cherrypy
import os, os.path
from controller.switch_controller import SwitchController


class AjaxInterface(object):
    @cherrypy.expose
    def index(self):
        return file('index.html')


class RestInterface(object):
    exposed = True
    controller = SwitchController()

    def _cp_dispatch(self, vpath):
        if len(vpath) == 2:
            cherrypy.request.params['switch'] = vpath.pop(0)

            if vpath.pop(0) == "on":
                cherrypy.request.params['on'] = "True"

    def index(self, switch="All", on="False"):
        if bool(on):
            if switch == "All":
                self.controller.switch_on(0)
            else:
                self.controller.switch_on(int(switch))
        else:
            if switch == "All":
                self.controller.switch_off(0)
            else:
                self.controller.switch_off(int(switch))

        return "Set state of " + switch + " to " + on

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    webapp = AjaxInterface()
    webapp.generator = RestInterface()
    cherrypy.quickstart(webapp, '/', conf)
