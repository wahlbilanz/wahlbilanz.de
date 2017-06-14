import re
import yaml
import sys

legislatur = re.compile('\\s*\* \[Legislaturperiode: (\\d+) \(([0-9-]+)\)\]\((.*)\)')
keyvalue = re.compile ('\\s*\* ([^:]+): (.*)')
linkitem = re.compile ('\\s*\* \[([^\]]+)\]\((.*)\)$')
doublelinkitem = re.compile ('\\s*\* \[([^\]]+)\]\((.*)\) \(\[([^\]]+)\]\((.*)\)\)$')

def get_value (s, f):
	m = keyvalue.match (s)
	if m:
		return m.group(2)
	else:
		raise IOError ("didn't match: " + s + " in " + f)



class Abstimmung:
	
	#title = ""
	#categories = []
	#tags = []
	
	#legislaturperiode = -1
	#legislaturperiode_year = ""
	#legislaturperiode_link = ""
	#sitzung = -1
	#abstimmung = -1
	
	#links = {}
	#data = {}
	#documents = {}
	
	#ergebnis = {}
	
	#preview = ""
	
	#def parse_ids (self, content):
		#for c in content:
			#if "* [Legislaturperiode" in c:
				#m = legislatur.match (c)
				#if m:
					#self.legislaturperiode = int (m.group(1))
					#self.legislaturperiode_year = m.group(2)
					#self.legislaturperiode_link = m.group(3)
			#if "* Bundestagssitzung:" in c:
				#m = keyvalue.match (c)
				#if m:
					#self.sitzung = int (m.group(2))
			#if "* Abstimmung:" in c:
				#m = keyvalue.match (c)
				#if m:
					#self.abstimmung = int (m.group(2))
	
	#def parse_links:
	
	def parse_abstimmung (self, abstimmungsfile):
		front = ""
		content = []
		state = 0
		ydata = None
		with open(abstimmungsfile, 'r') as f:
			for line in f:
				if "---" in line and state == 0:
					state = 1
					continue
				if "---" in line and state == 1:
					state = 2
					continue
				if state == 1:
					if "layout" in line:
						front += "layout: abstimmung\n"
					else:
						front += line
				if state == 2:
					content.append (line)
			
			if state != 2:
				raise IOError ("couldn't parse file: " + abstimmungsfile)
			
			ncont = []
			for l in range (0, len(content) - 1):
				c = content[l]
				#print c
				if "* Namentliche Abstimmung:" in c:
					ncont.append ("abstimmung:")
				elif "* [Legislaturperiode:" in c:
					ncont.append (" legislaturperiode: 18")
				elif "* Bundestagssitzung:" in c:
					ncont.append (" bundestagssitzung: " + get_value (c, abstimmungsfile))
				elif "* Abstimmung: " in c:
					ncont.append (" abstimmung: " + get_value (c, abstimmungsfile))
				elif "* Links:" in c:
					ncont.append ("links:")
					cur = l + 1
					while content[cur][0] != '*':
						m = linkitem.match (content[cur])
						if m:
							ncont.append (" - title: " + m.group(1))
							ncont.append ("   url: " + m.group(2))
						else:
							if content[cur] != "    * \n":
								raise IOError ("didn't match: " + content[cur] + " in " + abstimmungsfile)
						cur = cur + 1
					l = cur - 1
				elif "* Data:" in c:
					ncont.append ("data:")
					cur = l + 1
					while content[cur][0] != '*':
						m = linkitem.match (content[cur])
						if m:
							ncont.append (" - title: " + m.group(1))
							ncont.append ("   url: " + m.group(2))
						else:
							raise IOError ("didn't match: " + content[cur] + " in " + abstimmungsfile)
						cur = cur + 1
					l = cur - 1
				elif "* Documents:" in c:
					ncont.append ("documents:")
					cur = l + 1
					while content[cur][0] != '*':
						m = doublelinkitem.match (content[cur])
						if m:
							ncont.append (" - title: " + m.group(1))
							ncont.append ("   url: " + m.group(2))
							ncont.append ("   local: " + m.group(4))
						else:
							raise IOError ("didn't match: " + content[cur] + " in " + abstimmungsfile)
						cur = cur + 1
					l = cur - 1
				elif "* Abstimmungsergebnis:" in c:
					cur = l + 1
					while content[cur][0] != '*':
						cur = cur + 1
					l = cur - 1
				elif "* Preview:" in c:
					ncont.append ("preview: |")
					cur = l + 1
					while cur < len (content) and content[cur][0] == '>':
						ncont.append ("    " + content[cur][1:].rstrip())
						cur = cur + 1
					l = cur
					
				#elif "" in c:
					#content.append ("")
				#elif "" in c:
					#content.append ("")
				#elif "" in c:
					#content.append ("")
				#elif "" in c:
					#content.append ("")
				#elif "" in c:
					#content.append ("")
			
			ret = front + "\n".join (ncont)
			return ret
			#ydata = yaml.load (front)
			
			#self.title = ydata["title"]
			#self.categories = ydata["categories"]
			#self.tags = ydata["tags"]
			
			#self.parse_ids (content)
			
			#if state > 0:
				#erg = "* Abstimmungsergebnis:\n"
				#for fraktion in fraktionen:
					#if fraktion in abst_dict[abstid]:
						#erg += "    * " + fraktion + ": " + str (abst_dict[abstid][fraktion]["gesamt"]) + "\n"
						#erg += "        * Ja: " + str (abst_dict[abstid][fraktion]["ja"]) + "\n"
						#erg += "        * Nein: " + str (abst_dict[abstid][fraktion]["nein"]) + "\n"
						#erg += "        * Enthaltung: " + str (abst_dict[abstid][fraktion]["enthaltung"]) + "\n"
						#erg += "        * Ungueltig: " + str (abst_dict[abstid][fraktion]["ungueltig"]) + "\n"
						#erg += "        * Nicht abgegeben: " + str (abst_dict[abstid][fraktion]["nichtabgegeben"]) + "\n"
				
				#content = content.replace ("* Preview", erg + "* Preview")
				
				#with open(jekyll_file, 'w') as f:
					#f.write ("---\n")
					#f.write (front)
					#f.write ("---\n")
					#f.write (content)


curfile = sys.argv[1]
#dest = sys.argv[2]

a = Abstimmung ()
neu = a.parse_abstimmung (curfile)
with open(curfile, 'w') as f:
	f.write ("---\n")
	f.write (neu)
	f.write ("\n---")



#print a.legislaturperiode
#print a.legislaturperiode_year
#print a.legislaturperiode_link
#print a.sitzung
#print a.abstimmung


