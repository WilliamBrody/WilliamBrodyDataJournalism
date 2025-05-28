import json


f1 = open("sanatized_data.csv", "r")
lines = f1.readlines()

dictionary ={}


for i in lines:
    i = i.split(',')


for i in range(len(lines)):
    lines[i] = lines[i].strip('\n')
    lines[i] = lines[i].split(',')


dictionary['Mh'] = {}
dictionary['Bx'] = {}
dictionary['Br'] = {}
dictionary['Qs'] = {}
dictionary['Si'] = {}
dictionary['Ny'] = {}

print(dictionary)

for i in range(len(lines)):
     if lines[i][1] == 'Citywide':
         dictionary['Ny'][lines[i][0]] = lines[i][6]
     if lines[i][2] == 'Manhattan':
         dictionary['Mh'][lines[i][0]] = lines[i][6]
     if lines[i][2] == 'Bronx':
         dictionary['Bx'][lines[i][0]] = lines[i][6]
     if lines[i][2] == 'Queens':
         dictionary['Qs'][lines[i][0]] = lines[i][6]
     if lines[i][2] == 'Staten Island':
         dictionary['Si'][lines[i][0]] = lines[i][6]
     if lines[i][2] == 'Brooklyn':
         dictionary['Br'][lines[i][0]] = lines[i][6]

print(dictionary)
'''
for i in range(1, len(lines)):
    for n in range(1, len(lines[i])):
        dictionary[lines[i][0]][lines[0][n]] = int(float(lines[i][n]))
#del dictionary[lines[0][0]]

dictionary['year'] = []
for i in dictionary['Canada']:
    dictionary['year'].append(i)
'''
print()
# Create the dictionary here

f1.close()

#Save the json object to a file
f2 = open("formatted_aq.json", "w")
json.dump(dictionary, f2, indent = 4)



f2.close()
