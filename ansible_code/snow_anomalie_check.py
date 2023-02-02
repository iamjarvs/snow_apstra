
import json
  
snow_f = open('tmp.json')
apstra_f = open('anomalie_result.json')
snow_data = json.load(snow_f)
apstra_data = json.load(apstra_f)

to_create_data = []

for anomalie in apstra_data["blueprint_anomalie_information"]:
    if anomalie[1] in str(snow_data):
        print(str(anomalie[0]) + " : Exists")
    else:
        tmp_list = {}
        tmp_list["type"] = anomalie[0]
        tmp_list["id"] = anomalie[1]
        tmp_list["device"] = anomalie[2]
        tmp_list["status"] = anomalie[3]
        to_create_data.append(tmp_list)

with open("to_create_data.data", "w") as file:
    # Write the data to the file
    file.write(str(to_create_data))

print(to_create_data)

snow_f.close()
apstra_f.close()