
dic = {}
votes =['b', 'a', 'b', 'a', 'c']
for name in votes:
  if dic.__contains__(name):
    dic[name] += 1
  else:
    dic[name] = 1
most_names = []
most = 0
for key in dic:
  if dic[key] > most:
    most = dic[key]
for key in dic:
  if dic[key] == most:
    most_names.append(key)
most_names.sort(reverse=True)
print most_names[0]
#for name in sorted(most_names,key=str.lower, reverse=True):
 # print name