
import sys
import yaml

class Abstimmung:
	
	data = {}
	
	def parse_abstimmung (self, abstimmungsfile):
		with open(abstimmungsfile, 'r') as f:
			for data in yaml.load_all (f):
				if data:
					self.data = data
					break
	
	
	def get_title (self):
		return self.data["title"]
	
	
	
	def get_categories (self):
		return self.data["categories"]
	
	def add_category (self, category):
		self.data["categories"].append (category)
	
	
	
	def get_tags (self):
		return self.data["tags"]
	
	def add_tag (self, tag):
		self.data["tags"].append (tag)
	
	
	
	
	
	
	def write_abstimmung (self, abstimmungsfile):
		with open(abstimmungsfile, 'w') as f:
			yaml.dump (self.data, f, explicit_start=True, default_flow_style=False)
			f.write ("---")
	
	
	



if __name__ == "__main__":
	curfile = sys.argv[1]
	a = Abstimmung ()
	neu = a.parse_abstimmung (curfile)
	print a.get_title ()

