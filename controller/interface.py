import cherrypy
import os, os.path
from switch_controller import SwitchController


class AjaxInterface(object):
    @cherrypy.expose
    def index(self):
        return file('index.html')


class RestInterface(object):
    exposed = True

    def __init__(self, controller):
        self.controller = controller

    def _cp_dispatch(self, vpath):
        if len(vpath) == 2:
            cherrypy.request.params['switch'] = vpath.pop(0)

            if vpath.pop(0) == "on":
                cherrypy.request.params['on'] = "True"

        return self

    def POST(self, switch="0", on="False"):
        if on == "True":
            print "Turning on " + switch
            self.controller.switch_on(int(switch))
        else:
            print "Turning off " + switch
            self.controller.switch_off(int(switch))

        return "Set state of " + switch + " to " + on

if __name__ == '__main__':
    with SwitchController() as controller:
        conf = {
            '/': {
                'tools.sessions.on': True,
                'tools.staticdir.root': os.path.abspath(os.getcwd())
            },
            '/api': {
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
        webapp.api = RestInterface(controller)
        cherrypy.config.update({
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 80
        })
        cherrypy.quickstart(webapp, '/', conf)