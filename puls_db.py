import sqlite3, re

DB_PATH = 'data/data.sqlite3'

class PulsDB:

	def __init__(self):
		self._db = sqlite3.connect(DB_PATH, check_same_thread=False)
		self._db.row_factory = sqlite3.Row
		self.dirty = True
	
	def _update(self, sql, data):
		cursor = self._db.cursor()
		cursor.execute(sql, data)		
		self._db.commit()
		self.dirty = True
		
	def _select_all(self, sql, data = ()):
		cursor = self._db.cursor()
		cursor.execute(sql, data)	
		return cursor.fetchall()

	def _select_one(self, sql, data = ()):
		cursor = self._db.cursor()
		cursor.execute(sql, data)	
		return cursor.fetchone()

	def end(self):
		self._db.close()
	
	def get_all_etagen(self):
		return self._select_all('''SELECT * FROM etage ORDER BY position;''')

	def get_all_zimmer(self, etage_link):
		return self._select_all('''SELECT * FROM zimmer WHERE etage_link = ? ORDER BY position;''', (etage_link,))
		
	def get_all_verbraucher(self, etage_link, zimmer_link):
		return self._select_all('''SELECT * FROM verbraucher WHERE etage_link = ? AND zimmer_link = ? ORDER BY position;''', (etage_link, zimmer_link))

	def get_etage(self, etage_link):
		return self._select_one('''SELECT * FROM etage WHERE etage_link = ?;''', (etage_link,))

	def get_zimmer(self, etage_link, zimmer_link):
		return self._select_one('''SELECT * FROM zimmer WHERE etage_link = ? AND zimmer_link = ?;''', (etage_link, zimmer_link))
			
	def get_verbraucher(self, etage_link, zimmer_link, verbraucher_link):
		return self._select_one('''SELECT * FROM verbraucher WHERE etage_link = ? AND zimmer_link = ? AND verbraucher_link = ?;''', (etage_link, zimmer_link, verbraucher_link))	

	def set_etage_eingeschaltet(self, etage_link, eingeschaltet):
		if re.match('[01]', eingeschaltet):
			self._update('''UPDATE etage SET eingeschaltet = ? WHERE etage_link = ?;''', (eingeschaltet, etage_link))		

	def set_zimmer_eingeschaltet(self, etage_link, zimmer_link, eingeschaltet):
		if re.match('[01]', eingeschaltet):
			self._update('''UPDATE zimmer SET eingeschaltet = ? WHERE etage_link = ? AND zimmer_link = ?;''', (eingeschaltet, etage_link, zimmer_link))		

	def set_verbraucher_eingeschaltet(self, etage_link, zimmer_link, verbraucher_link, eingeschaltet):
		if re.match('[01]', eingeschaltet):
			self._update('''UPDATE verbraucher SET eingeschaltet = ? WHERE etage_link = ? AND zimmer_link = ? AND verbraucher_link = ?;''', (eingeschaltet, etage_link, zimmer_link, verbraucher_link))
			
	def set_verbraucher_helligkeit(self, etage_link, zimmer_link, verbraucher_link, helligkeit):
		if re.match('[0-9]{1,4}', helligkeit) and int(helligkeit) >= 0 and int(helligkeit) <= 4096:
			self._update('''UPDATE verbraucher SET helligkeit = ? WHERE etage_link = ? AND zimmer_link = ? AND verbraucher_link = ?;''', (helligkeit, etage_link, zimmer_link, verbraucher_link))
			
	def set_verbraucher_modus(self, etage_link, zimmer_link, verbraucher_link, modus):
		if re.match('[012]', modus):
			self._update('''UPDATE verbraucher SET modus = ? WHERE etage_link = ? AND zimmer_link = ? AND verbraucher_link = ?;''', (modus, etage_link, zimmer_link, verbraucher_link))
			
	def get_initial_pwm_values(self):
		values = dict()
		allVerbraucher = self._select_all('''SELECT modul, port FROM verbraucher WHERE typ == "L";''')
		for verbraucher in allVerbraucher:			
			values[(verbraucher['modul'], verbraucher['port'])] = 0
		return values

	def get_desired_pwm_values(self):
		values = dict()
		allVerbraucher = self._select_all('''SELECT v.modul, v.port, v.helligkeit, v.eingeschaltet, z.eingeschaltet AS zimmer_eingeschaltet, e.eingeschaltet AS etage_eingeschaltet FROM etage e JOIN zimmer z ON e.etage_link = z.etage_link JOIN verbraucher v ON z.zimmer_link = v.zimmer_link WHERE v.typ == "L";''')
		for verbraucher in allVerbraucher:			
			helligkeit = verbraucher['helligkeit'] if verbraucher['etage_eingeschaltet'] == 1 and verbraucher['zimmer_eingeschaltet'] == 1 and verbraucher['eingeschaltet'] == 1 else 0
			values[(verbraucher['modul'], verbraucher['port'])] = helligkeit
		self.dirty = False
		return values
		
	def get_initial_relay_values(self):
		values = dict()
		allVerbraucher = self._select_all('''SELECT port FROM verbraucher WHERE typ == "S";''')
		for verbraucher in allVerbraucher:			
			values[verbraucher['port']] = 0
		return values

	def get_desired_relay_values(self):
		values = dict()
		allVerbraucher = self._select_all('''SELECT v.port, v.eingeschaltet, z.eingeschaltet AS zimmer_eingeschaltet, e.eingeschaltet AS etage_eingeschaltet FROM etage e JOIN zimmer z ON e.etage_link = z.etage_link JOIN verbraucher v ON z.zimmer_link = v.zimmer_link WHERE v.typ == "S";''')
		for verbraucher in allVerbraucher:			
			eingeschaltet = verbraucher['eingeschaltet'] if verbraucher['etage_eingeschaltet'] == 1 and verbraucher['zimmer_eingeschaltet'] == 1 else 0
			values[verbraucher['port']] = eingeschaltet
		self.dirty = False
		return values
