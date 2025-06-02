# flask --app data_server run
from flask import Flask
from flask import request
from flask import render_template
import json

f = open("data/formatted_aq.json", "r")
f = json.load(f)

app = Flask(__name__, static_url_path='', static_folder='static')


"""
QUESTIONS FOR MR. GOHDE:
- how should i embedd images in my about page
    - put them in the static folder, and then link normally (no jinja)
    - what else should really be in about page?
        - what the project is
        - vocab
        - link to data
        - prototypes
        - etc
    
    
- how do i go about generating the dynamic text???
    - if statements
    - dynamically generate adjectives
- what should be in my footer?(what even is a footer)
    - link to data
    - will brody data journalism 
    - etc
    
    - do i put data source and my contact info?
- how should i clean up my graph (all the plots are too close together)
"""

@app.route('/')
def index():
    all_boroughs = []
    for key in f:
        all_boroughs.append(key)

    # func for getting years for dropdown
    all_years = []
    for i in f["Ny"]:
        all_years.append(i)
    # for passing the year to the index
    requestedYear = request.args.get('year')
    
    if requestedYear == None:
        print(type(requestedYear))
        print("request average!")
        requestedYear = "NYC average from year-year"

    print(requestedYear)

    brightData = [] # order Mh, Br, Qs, Bx, Si ranging 0-15 to 0-100
    if requestedYear != 'NYC average from year-year':
        brightData.append(0 + ((100 - 0) / (15 - 0)) * (float(f['Mh'][requestedYear][0]) - 0))
        brightData.append(0 + ((100 - 0) / (15 - 0)) * (float(f['Br'][requestedYear][0]) - 0))
        brightData.append(0 + ((100 - 0) / (15 - 0)) * (float(f['Qs'][requestedYear][0]) - 0))
        brightData.append(0 + ((100 - 0) / (15 - 0)) * (float(f['Bx'][requestedYear][0]) - 0))
        brightData.append(0 + ((100 - 0) / (15 - 0)) * (float(f['Si'][requestedYear][0]) - 0))
    else:
        brightData = [0, 0, 0, 0, 0]
        for i in range(2009, 2023):
            n = str(i)
            brightData[0] += 0 + ((100 - 0) / (15 - 0)) * (float(f['Mh'][n][0]) - 0)
            brightData[1] += 0 + ((100 - 0) / (15 - 0)) * (float(f['Br'][n][0]) - 0)
            brightData[2] += 0 + ((100 - 0) / (15 - 0)) * (float(f['Qs'][n][0]) - 0)
            brightData[3] += 0 + ((100 - 0) / (15 - 0)) * (float(f['Bx'][n][0]) - 0)
            brightData[4] += 0 + ((100 - 0) / (15 - 0)) * (float(f['Si'][n][0]) - 0)
        brightData[0] = brightData[0] / 15
        brightData[1] = brightData[1] / 15
        brightData[2] = brightData[2] / 15
        brightData[3] = brightData[3] / 15
        brightData[4] = brightData[4] / 15

    print(brightData)

    return render_template('index.html', all_borough=all_boroughs, all_years=all_years, requestedYear=requestedYear, boroughBright=brightData)


@app.route('/about')
def about():
    # so for macro we will do a map with the average data for each borough
    # and for the micro we will have a graph with summer vs winter vs avg vs avg for rest of city
    return render_template('about.html')

@app.route('/borough')
def borough():
    requestedborough = request.args.get('borough')
    print(requestedborough)
    # average, summer, winter, nyc avg
    polGraphDat = [[],[],[],[]]
    for i in range(2009, 2023):
        polGraphDat[0].append(float(f[requestedborough][str(i)][0]))
        polGraphDat[1].append(float(f[requestedborough][str(i)][1]))
        polGraphDat[2].append(float(f[requestedborough][str(i)][2]))
        polGraphDat[3].append(float(f['Ny'][str(i)][2]))
    return render_template('micro.html', borough=requestedborough, endpoints=polGraphDat)



app.run(debug=True, port=25565)
