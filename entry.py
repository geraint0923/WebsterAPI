import urllib2
import re
import xml.etree.ElementTree as et


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
		dt_list = df.findall("dt");
		for dt in dt_list:
			r = self.__trim_def(dt.text);
			rr = self.__parse_sx(dt);
			if r:
				if rr:
					self.word_def.append(r + ": " + rr);
				else:
					self.word_def.append(r);
			else:
				if rr:
					self.word_def.append(rr);
#			print dt.text;

	def print_word(self):
		print self.word_name
		print "type:", self.word_type;
		num = 1;
		print "definitions:";
		if len(self.word_def) == 0:
			print "None";
		for item in self.word_def:
#			print "(" + str(num) + ")",item;
			print "(%d) %s" % (num, item);
			num += 1;


def look_up_word(name, key):
	url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/" + name + "?key=" + key;
#	print url;
	content = urllib2.urlopen(url).read();
	content = re.sub("</?fw>", "", content);
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
				word.print_word();
				res.append(word);
		
	return res;
