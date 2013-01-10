import urllib2
import re
import xml.etree.ElementTree as et
import sys

old_stdout = sys.stdout;

def restore_stdout():
	sys.stdout = old_stdout;

def reopen_stdout(filename):
	sys.stdout = open(filename, "w+");


class word_entry:
	def __init__(self, n):
		self.word_name = n;
		self.word_type = "";
		self.word_def = [];

	def __del__(self):
		pass;

	def __trim_def(self, s):
		pattern = re.compile("^:(.*[^:]+):*");
		if s:
			res = pattern.findall(s);
			if len(res) > 0:
				return res[0];
		return None;

	def __parse_sx(self, dt):
		sx_list = dt.findall("sx");
		begin = 0;
		res = None;
		for item in sx_list:
			if begin == 0:
				begin = 1;
				res = "";
			else:
				res += ", ";
			res += item.text;
		return res;

	def parse_def(self, df):
#		dt_list = df.findall("dt");
		tag = "";
		sec = ""; #3
		subsec = ""; #3
		subsubsec = ""; #4
		deep = 0;
		for dt in df:
			if dt.tag == "vt":
				if dt.text:
					self.word_def.append(dt.text);
				continue;
			if dt.tag == "dt":
				tag = "%s%s%s " %(sec, subsec, subsubsec);
				r = self.__trim_def(dt.text);
				rr = self.__parse_sx(dt);
				if r == None and dt.text:
					pattern = re.compile("^([^:]+)");
					ff = pattern.findall(dt.text);
					if len(ff) > 0:
						if len(ff[0]) == len(dt.text):
							r = dt.text;
				if r:
					if rr:
						self.word_def.append(tag + r + ": " + rr);
					else:
						self.word_def.append(tag + r);
				else:
					if rr:
						self.word_def.append(tag + rr);
				if r or rr:
					if len(sec) == 3:
						sec = "   ";
					else:
						sec = "";
					if len(subsec) == 3:
						subsec = "   ";
					else:
						subsec = "";
					if len(subsubsec) == 4:
						subsubsec = "    ";
					else:
						subsubsec = "";
				continue;
			if dt.tag == "sn":
				if dt.text:
					sl = dt.text.split(" ");
#					print "\""+dt.text+"\"",len(sl);
					ll = 9;
					for l in sl:
						if ll > len(l):
							ll = len(l);
#						print "haha:","\""+l+"\"", len(l);
					if len(sl) > 1 and ll > 0:   # like "2 a"
						sec = "%2s." % sl[0];
						subsec = "%2s." % sl[1];
						subsubsec = "";
					else:
						try:
							num = int(sl[0]);
							sec = "%2d." % num;
							subsec = "";
							subsubsec = "";
						except ValueError:
							subsec = "%2s." % sl[0];
							sec = "   ";
							subsubsec = "";
				snp = dt.find("snp");
				if snp != None:
					if snp.text:
						subsubsec = "%4s" % snp.text;
#						sec = "   ";
#						subsec = "   ";

#			print dt.text;

	def print_word(self, fp):
		fp.write(self.word_name+"\n");
		fp.write("type: "+self.word_type+"\n");
		fp.write("definitions:"+"\n");

		if len(self.word_def) == 0:
			fp.write("None\n");
		for item in self.word_def:
			print item;
			fp.write(item+"\n");
#		print self.word_name
#		print "type:", self.word_type;
#		print "definitions:";
#		if len(self.word_def) == 0:
#			print "None";
#		for item in self.word_def:
#			print "%s" % item;


def look_up_word(name, fp, key):
	url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/" + name + "?key=" + key;
#	print url;
	content = urllib2.urlopen(url).read();
	content = re.sub("</?fw>", "", content);
	content = content.replace("<un>", "");
	content = content.replace("</un>", "");
	content = content.replace("<vi>", "[");
	content = content.replace("</vi>", "]");
	content = content.replace("<it>", "");
	content = content.replace("</it>", "");
#	print content;
	res = [];

	root = et.fromstring(content);
	if len(root):
#		print root;
		entry_list = root.findall("entry");
#		print entry_list;
		for entry in entry_list:
			if entry.find("ew").text.lower() == name.lower():
#				print "***********************************";
				print "";
				word = word_entry(entry.find("ew").text);
				word.word_type = entry.find("fl").text;
				word.parse_def(entry.find("def"));
				word.print_word(fp);
				fp.write("\n");
				res.append(word);
		
	return res;
