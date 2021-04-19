#!/usr/bin/env python3

import sys
import yaml
import os
from yaml.representer import SafeRepresenter

#def unicode_representer (dumper, uni):
	#node = yaml.ScalarNode (tag = u'tag:yaml.org,2002:str', value = uni)
	#return node
#yaml.add_representer(unicode, unicode_representer)
yaml.add_representer(str, SafeRepresenter.represent_str)

class Abstimmung:

	data = {}

	def parse_abstimmung (self, abstimmungsfile):
		with open(abstimmungsfile, 'r') as f:
			for data in yaml.load_all (f):
				if data:
					self.data = data
					break

	def __init__(self):
		self.data = {}


	def get_title (self):
		return self.data["title"]

	def set_title (self, title):
		self.data["title"] = title




	def get_legislaturperiode (self):
		return self.data["abstimmung"]["legislaturperiode"]

	def set_legislaturperiode (self, legislaturperiode):
		if not "abstimmung" in self.data:
			self.data["abstimmung"] = {}
		self.data["abstimmung"]["legislaturperiode"] = legislaturperiode




	def get_bundestagssitzung (self):
		return self.data["abstimmung"]["bundestagssitzung"]

	def set_bundestagssitzung (self, bundestagssitzung):
		if not "abstimmung" in self.data:
			self.data["abstimmung"] = {}
		self.data["abstimmung"]["bundestagssitzung"] = bundestagssitzung




	def get_abstimmung (self):
		return self.data["abstimmung"]["abstimmung"]

	def set_abstimmung (self, abstimmung):
		if not "abstimmung" in self.data:
			self.data["abstimmung"] = {}
		self.data["abstimmung"]["abstimmung"] = abstimmung





	def get_datum (self):
		return self.data["abstimmung"]["datum"]

	def set_datum (self, datum):
		if not "abstimmung" in self.data:
			self.data["abstimmung"] = {}
		self.data["abstimmung"]["datum"] = datum





	def get_categories (self):
		return self.data["categories"]

	def set_categories (self, categories):
		self.data["categories"] = categories

	def add_category (self, category):
		if not "categories" in self.data:
			self.data["categories"] = []
		self.data["categories"].append (category)



	def get_tags (self):
		return self.data["tags"]

	def set_tags (self, tags):
		self.data["tags"] = tags

	def add_tag (self, tag):
		if not "tags" in self.data:
			self.data["tags"] = []
		self.data["tags"].append (tag)




	def get_abstimmungs_ergebnisse (self):
		return self.data["ergebnis"]

	def set_abstimmungs_ergebnisse (self, tag):
		self.data["ergebnis"] = (tag)


	#######################################################################
	#
	# DATA FILES ...
	#
	# sind Dateien, die Daten zu einer Bestimmten Abstimmung enthalten.
	# Jedes "data_file" Objekt ist ein dict und sollte die folgenden
	# keys enthalten:
	# - titel: Menschenlesbare Beschreibung
	# - url: Link zur Datei
	#
	# get_data_files returns alle bekannten data_files.
	def get_data_files (self):
		if not "data" in self.data:
			self.data["data"] = []
		return self.data["data"]
	#
	# set_data_files ueberschreibt alle data_files mit einem neuen array
	def set_data_files (self, data):
		self.data["data"] = data
	#
	# add_data_file fuegt ein neues "data_file" Objekt hinzu
	def add_data_file (self, data_file):
		if not "data" in self.data:
			self.data["data"] = []
		self.data["data"].append (data_file)
	#
	#######################################################################




	def get_documents (self):
		return self.data["documents"]

	def set_documents (self, documents):
		self.data["documents"] = documents

	def add_document (self, document):
		if not "documents" in self.data:
			self.data["documents"] = []
		self.data["documents"].append (document)




	def get_links (self):
		return self.data["links"]

	def set_links (self, links):
		self.data["links"] = links

	def add_link (self, links):
		if not "links" in self.data:
			self.data["links"] = []
		self.data["links"].append (links)






	def get_preview (self):
		return self.data["preview"]

	def set_preview (self, preview):
		self.data["preview"] = (preview)







	def write_abstimmung (self, abstimmungsfile):
		self.data["layout"] = "abstimmung"

		if not os.path.exists (os.path.dirname (abstimmungsfile)):
			os.makedirs (os.path.dirname (abstimmungsfile))

		with open(abstimmungsfile, 'w') as f:
			yaml.dump (self.data, f, explicit_start=True, default_flow_style=False, encoding='utf-8', allow_unicode=True)
			f.write ("---")






if __name__ == "__main__":
	curfile = sys.argv[1]
	a = Abstimmung ()
	neu = a.parse_abstimmung (curfile)
	print (a.get_title ())

