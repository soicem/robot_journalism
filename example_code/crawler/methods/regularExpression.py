import re

#p_date = re.compile(r'(\d{1,2})[/-](\d{1,2})[/-](\d{1,4})')
p_date = re.compile(r'(\d{1,2}[/-]\d{1,2}[/-]\d{1,4})')
target = "11/12/98 \
   0/0/0\
  25/02/1977"

print(p_date.findall(target))

target2 = "2017-04-07T23:24:45+09:00"
p_date = re.compile(r'(\d{1,4}[/-]\d{1,2}[/-]\d{1,2}[T]\d{1,2}[/:]\d{1,2}[/:]\d{1,2}[+]\d{1,2}[/-:]\d{1,2})')
print(p_date.findall(target2))