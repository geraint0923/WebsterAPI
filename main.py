import entry
import sys
import codecs


file_prefix = "data/";
file_suffix = ".txt";
key = "";

f = codecs.open("input.txt", "r", "utf-8");
fp = None;
lines = f.readlines();
check = 0;

for line in lines:
	print line;
	line = line[:-1];
	if len(line) <= 0:
		continue;
	if line.startswith("#"):
		if line.startswith("#begin"):
			check = 1;
			continue;
		if line.startswith("#end"):
			check = 0;
			break;
		line = line.replace("#", "");
		if fp != None:
			fp.close();
		fp = codecs.open(file_prefix + line + file_suffix, "w+", "utf-8");
		continue;
	if check == 1 and fp != None:
		entry.look_up_word(line, fp, key);
		fp.write("\n\n");

if fp != None:
	fp.close();

#fp = codecs.open("oo", "w+", "utf-8");
#entry.look_up_word("hostility", fp, key);

#entry.look_up_word("test", fp, key);
#print a.name
