import sys
filename = sys.argv[-1]

d = {}
with open(filename, 'r') as f:
  for line in f:
#    print line
    d[line.split()[0]] = line.split()[1]

for key, value in d.iteritems():
  for r in value.split(","):
    print "%s,%s" % (key, r)


