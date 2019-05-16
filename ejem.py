import re
patternStock = re.compile(r"^\b(10{0,2}|[1-9]{1,2})\b$")
string = "890000000000000"
matchobj = patternStock.search(string)
s = matchobj

print(s)