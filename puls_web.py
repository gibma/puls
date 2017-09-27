from lib.bottle import Bottle, run, view, static_file, template, request, response, abort, error

class PulsWeb:
	
	def __init__(self, puls_db, name):
		self._db = puls_db
		self._app = Bottle()
		self._define_routes()
		self._name = name
		
	def _define_routes(self):
		# GET (static)
		self._app.route('/favicon.ico', 									method="GET",  callback=self._serve_favicon)
		self._app.route('/<type:re:css|fonts|js>/<filename>', 				method="GET",  callback=self._serve_static)
		
		# GET
		self._app.route('/', 												method="GET",  callback=self._get_index)
		self._app.route('/<etage_link>', 									method="GET",  callback=self._get_etage)
		self._app.route('/<etage_link>/<zimmer_link>', 						method="GET",  callback=self._get_zimmer)
		self._app.route('/<etage_link>/<zimmer_link>/<verbraucher_link>', 	method="GET",  callback=self._get_verbraucher)
		
		# POST
		self._app.route('/<etage_link>/eingeschaltet', 									method="POST", callback=self._set_etage_eingeschaltet)
		self._app.route('/<etage_link>/<zimmer_link>/eingeschaltet', 					method="POST", callback=self._set_zimmer_eingeschaltet)
		self._app.route('/<etage_link>/<zimmer_link>/<verbraucher_link>/eingeschaltet', method="POST", callback=self._set_verbraucher_eingeschaltet)
		self._app.route('/<etage_link>/<zimmer_link>/<verbraucher_link>/helligkeit', 	method="POST", callback=self._set_verbraucher_helligkeit)
		self._app.route('/<etage_link>/<zimmer_link>/<verbraucher_link>/modus', 		method="POST", callback=self._set_verbraucher_modus)
		
		self._app.error_handler[404] = self._error404
		self._app.error_handler[405] = self._error404
		
	def start(self):
		run(self._app, host='localhost', port=80, debug=True)		
		
	def _serve_static(self, type, filename):
		return static_file(type + '/' + filename, root="./")

	def _serve_favicon(self):
		return static_file("favicon.ico", root="./images/")
	
	@view('index')
	def _get_index(self):
		allEtagen = self._db.get_all_etagen()
		return dict(haus = self._name, allEtagen = allEtagen)

	@view('etage')
	def _get_etage(self, etage_link):
		etage = self._db.get_etage(etage_link)
		if etage is None:
			abort(404, f"Die Etage \"{etage_link}\" existiert nicht!")
		allZimmer = self._db.get_all_zimmer(etage_link)
		return dict(haus = self._name, etage = etage, allZimmer = allZimmer)

	@view('zimmer')
	def _get_zimmer(self, etage_link, zimmer_link):
		etage = self._db.get_etage(etage_link)
		if etage is None:
			abort(404)
		zimmer = self._db.get_zimmer(etage_link, zimmer_link)
		if zimmer is None:
			abort(404)
		allVerbraucher = self._db.get_all_verbraucher(etage_link, zimmer_link)
		return dict(haus = self._name, etage = etage, zimmer = zimmer, allVerbraucher = allVerbraucher)
	
	@view('verbraucher')
	def _get_verbraucher(self, etage_link, zimmer_link, verbraucher_link):
		etage = self._db.get_etage(etage_link)
		if etage is None:
			abort(404)
		zimmer = self._db.get_zimmer(etage_link, zimmer_link)
		if zimmer is None:
			abort(404)
		verbraucher = self._db.get_verbraucher(etage_link, zimmer_link, verbraucher_link)
		if verbraucher is None:
			abort(404)
		# TODO: Modi in DB schreiben
		modi = [(0, "Normal"), (1, "Kerzenflackern"), (2, "Gaslicht")]
		return dict(haus = self._name, etage = etage, zimmer=zimmer, verbraucher=verbraucher, modi=modi)

	def _set_etage_eingeschaltet(self, etage_link):
		self._db.set_etage_eingeschaltet(etage_link, request.params.get('value'))

	def _set_zimmer_eingeschaltet(self, etage_link, zimmer_link):
		self._db.set_zimmer_eingeschaltet(etage_link, zimmer_link, request.params.get('value'))

	def _set_verbraucher_eingeschaltet(self, etage_link, zimmer_link, verbraucher_link):
		self._db.set_verbraucher_eingeschaltet(etage_link, zimmer_link, verbraucher_link, request.params.get('value'))
	
	def _set_verbraucher_helligkeit(self, etage_link, zimmer_link, verbraucher_link):
		self._db.set_verbraucher_helligkeit(etage_link, zimmer_link, verbraucher_link, request.params.get('value'))
	
	def _set_verbraucher_modus(self, etage_link, zimmer_link, verbraucher_link):
		self._db.set_verbraucher_modus(etage_link, zimmer_link, verbraucher_link, request.params.get('value'))				
		
	@view('error404')
	def _error404(self, error):
		return dict(haus = self._name, message=error.body)
