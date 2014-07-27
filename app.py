#!/usr/bin/env python3

# Clear out old session lockfiles BEFORE importing cherry
#import os
#for f in os.listdir("sessions/"):
#	if "lock" in f:
#		os.remove("sessions/%s" % f)

import sys
import os
import cherrypy
import json
import sqlite3
from jinja2 import Environment, FileSystemLoader

if __name__ == '__main__' or 'uwsgi' in __name__:
	
	appdir = "/path/to/appdir"
	appconf = {
		'/': {
			#'tools.proxy.on':True,
			#'tools.proxy.base': conf["base"]["url"],
			'tools.sessions.on':True,
			'tools.sessions.storage_type':'file',
			'tools.sessions.storage_path':appdir+'/sessions/',
			'tools.sessions.timeout':525600,
			'request.show_tracebacks': True
		},
		'/media': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': appdir+"/static/"
		}
	}
	
	cherrypy.config.update({
		'server.socket_port':3000,
		'server.thread_pool':1,
		'server.socket_host': '0.0.0.0',
		'sessionFilter.on':True,
		'server.show.tracebacks': True
	})
	
	cherrypy.server.socket_timeout = 5
	
	class database(object):
		def __init__(self):
			pass
		
		def openDB(self):
			db = sqlite3.connect("db.sqlite", isolation_level=None)
			db.row_factory = self.dict_factory
			return db
			
		def dict_factory(self, cursor, row):
			d = {}
			for idx, col in enumerate(cursor.description):
				d[col[0]] = row[idx]
			return d
		
		def execute(self, sql, params=None):
			db = self.openDB()
			cursor = db.cursor()
			if params:
				cursor.execute(sql, params)
			else:
				cursor.execute(sql)
			data = cursor.fetchall()
			cursor.close()
			db.close()
			return data
	
	env = Environment(loader=FileSystemLoader(appdir+"/templates/"))
	db = database()
	
	def render(template, args):
		#templateCache = pysite.cacheTemplates()
		defaults = {"templates":pysite.templateCache}
		for item in args:
			defaults[item] = args[item]
		return quickRender(template, defaults)
	
	def quickRender(template, args):
		template = env.get_template(template)
		return template.render(args)
	
	class siteRoot(object):
		def __init__(self):
			print("Siteroot init!")
			self.templateCache = self.cacheTemplates()
		
		def cacheTemplates(self):
			templateFiles = os.listdir("jstemplates/")
			templateList = []
			nameList = []
			for item in templateFiles:
				name = item.split(".")
				templateList.append({"name":name[0],"content":open("jstemplates/"+item,"r").read().replace("\t", "").replace("\n","")})
				nameList.append(name[0])
			return quickRender("templates.html", {"names":json.dumps(nameList), "templates":templateList})
		
		@cherrypy.expose
		def index(self):
			return render("html.html", {})
	
	class api(object):
		def __init__(self):
			pass
		@cherrypy.expose
		def version(self):
			return json.dumps({"version":1.0})
		
		@cherrypy.expose
		def getSomething(self):
			return json.dumps({"people": [
				{"name":"Dave", "color":"blue"},
				{"name":"Bob", "color":"red"},
			]})
	
	pysite = siteRoot()
	pysite.api = api()
	
	print( "Ready to start application" )
	
	if(len(sys.argv)>1 and sys.argv[1]=="test"):
		print("test!")
		application = cherrypy.quickstart(pysite, '/', appconf)
	else:
		sys.stdout = sys.stderr
		cherrypy.config.update({'environment': 'embedded'})
		application = cherrypy.tree.mount(pysite, "/", appconf)
