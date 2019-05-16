import re
pattern, string = r"^\b(10{0,2}|[1-9]{1,2})\b$", "89"
matchobj = re.search(pattern, string)

if matchobj:
    print(matchobj.start())