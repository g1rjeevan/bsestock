import json

import cherrypy
import redis
import os

import cherrypy
import time
from jinja2 import Environment, FileSystemLoader
from downloaderbhavfile import getBhav

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
env=Environment(loader=FileSystemLoader(CUR_DIR),
trim_blocks=True)

class Index(object):

    @cherrypy.expose()
    def index(self):
        redis_server = getBhav()
        bseobjs = redis_server.get('bhavcopy')
        bseobjtop = redis_server.get('bsetop')
        bsedatestr = redis_server.get('datestr')
        bseobjs = json.loads(bseobjs)
        bseobjtop = json.loads(bseobjtop)
        template = env.get_template('index.html')
        # RENDER TEMPLATE PASSING IN DATA
        print bsedatestr,"sdds"
        try:
            bsedatestr = time.strftime("%d %b %Y",time.strptime(bsedatestr, "%Y-%m-%d"))
        except:
            bsedatestr = time.strftime("%d %b %Y", time.strptime(bsedatestr, "%Y-%m-%d  %H:%M:%S"))

        return template.render(title='Zerodha - BSE', description='This is a dev page',
                               list_header=bsedatestr, bseobjs=bseobjs,bseobjtop=bseobjtop, site_title="Stock list")

config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    },
    '/static': {
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static',
    }
}

if __name__=="__main__":
    cherrypy.quickstart(Index(), '/', config=config)

