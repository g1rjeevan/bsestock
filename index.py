import json

import cherrypy
import redis
import os

import cherrypy
import time
from jinja2 import Environment, FileSystemLoader

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
env=Environment(loader=FileSystemLoader(CUR_DIR),
trim_blocks=True)

class Index(object):

    @cherrypy.expose()
    def index(self):
        redis_server = redis.Redis("localhost")
        bseobjs = redis_server.get('bhavcopy')
        bseobjtop = redis_server.get('bsetop')
        bsedatestr = redis_server.get('datestr')
        bseobjs = json.loads(bseobjs)
        bseobjtop = json.loads(bseobjtop)
        template = env.get_template('index.html')
        # RENDER TEMPLATE PASSING IN DATA
        bsedatestr = time.strftime("%d %b %Y",time.strptime(bsedatestr, "%Y-%m-%d"))
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

    ######################
    # df = pandas.read_csv(destination + '\EQ' + date_str + '.CSV', dtype={
    #     "SC_CODE": str,
    #     "SC_NAME": str,
    #     "SC_TYPE": str,
    #     "OPEN": float,
    #     "HIGH": float,
    #     "LOW": float,
    #     "CLOSE": float
    # })
    #
    # results = []
    #
    # for (SC_CODE, SC_NAME, SC_TYPE,OPEN,HIGH, LOW,CLOSE), bag in df.groupby(["SC_CODE", "SC_NAME", "SC_TYPE","OPEN","HIGH","LOW","CLOSE"]):
    #     contents_df = bag.drop(["SC_CODE", "SC_NAME", "SC_TYPE","OPEN","HIGH","LOW","CLOSE"], axis=1)
    #     results.append(OrderedDict([('code', SC_CODE), ('name', SC_NAME), ('type', SC_TYPE),
    #                                  ('high', HIGH),('low', LOW),('close', CLOSE)]))
    # data = json.dumps(results)
    #
    # print data[3]
    #########################
    # data = [dict(zip(i, row)) for i, row in contents_df.iterrows()]
    # data.pop(0)
    # s = json.dumps(data)("CODE", SC_CODE),
    #                                 ("NAME", SC_NAME),
    #                                 ("TYPE", SC_TYPE),
    #                                 ("HIGH", HIGH),
    #                                 ("LOW", LOW),
    #                                 ("CLOSE", CLOSE)
    # print (s)
    # with open(destination + '\EQ' + date_str + '.CSV', 'r') as f:
    #     reader = csv.reader(f, delimiter=';')
    #     data_list = list()
    #     for row in reader:
    #         data_list.append(row)
    # data = [dict(zip(data_list[0], row)) for row in data_list]
    # data.pop(0)
    # s = json.dumps(data)
    # print (s)
    # chunksize = 1000 ** 822
    # for chunk in pandas.read_csv(destination + '\EQ' + date_str + '.CSV', chunksize=chunksize):
    #     results.append(chunk)
    # print results
    # Read the file
    # data = pandas.read_csv(destination + '\EQ' + date_str + '.CSV', low_memory=False)
    # # for df in data.iterrows():
    # #     print(df)
    # #     time.sleep(1)
    # s = pandas.json.dumps(data)
    # print (s)