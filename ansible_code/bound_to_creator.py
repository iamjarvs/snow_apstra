import json
newlist = []

data_parse = open('tmp.json')
data = json.load(data_parse)
data_parse.close()

for node in data["items"]:
    newlist.append('{ "system_id": "%s" }' % node['leaf']['id'])

print(newlist)

