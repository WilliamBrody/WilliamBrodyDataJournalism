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

"""
TODO:
- need to actually flesh out about page
- clean up small things
- VIDEO!!!
- BIG TAKEAWAYS
- make header h1 tag gud
- UNITS
"""

boroughs = {
    'Mh' : 'Manhattan',
    'Bx' : 'Bronx',
    'Qs' : 'Queens',
    'Br' : 'Brooklyn',
    'Si' : 'Staten Island',
    'Ny' : 'New York City'
}

def giveSeverity(n: float):
    if n < 33.33:
        return 'mild'
    if n > 33.33 and n < 66.66:
        return 'moderate'
    if n > 66.66:
        return 'severe'
    return 'giveSeverity ERROR DEFAULT 1'
def giveSeverity115(n: float):
    if n <= 5:
        return 'mild'
    if n > 5 and n < 10:
        return 'moderate'
    if n >= 10:
        return 'severe'
    return 'giveSeverity ERROR DEFAULT 1'

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
        requestedYear = '2009-2023'

    
    
    
    # Start the nightmare of how to do the dynamic text
    '''
    script:
    for __(year)__ __(lowest)__ had a __(low, moderate, high)__ polution.  __(second lowest)__ had a
    __(low, moderate, high)__ higher level of pollution. __(third lowest)__ and __(fourth lowest)__ followed.
    __(fith lowest)__ was last with a pollution of [[DATA]]
    
    the most annoying part of this is keeping track of which 
    datapoint goes with which borogh without messing up the order 
    in a way where we can know the order of how polluted a borogh is.
    
    this goes off of brightness data, not because thats a good idea, but because thats what ive already implemented
    
    I have absolutely no idea how to do this, but here goes:
    '''
    # map data
    
    borough = ['Mh', 'Br', 'Qs', 'Bx', 'Si']
    zDat = list(sorted(list(zip(brightData, borough))))
    print(zDat)
    # this creates a list of tuples that we will use to do the text generation
    dynamic_text = "For " + str(requestedYear) + ", " + boroughs[zDat[0][1]] + " had a " + giveSeverity(zDat[0][0]) + " pollution level, which was the best of all five borough. "
    dynamic_text = dynamic_text + boroughs[zDat[1][1]] + " came in second, with a " + giveSeverity(zDat[1][0]) + " level of pollution. "
    dynamic_text = dynamic_text + boroughs[zDat[2][1]] + " and " + boroughs[zDat[3][1]] + " came in 3rd and 4th place. "
    dynamic_text = dynamic_text + boroughs[zDat[4][1]] + " was the most polluted."
    
    
    return render_template('index.html', all_borough=all_boroughs, all_years=all_years, requestedYear=requestedYear, boroughBright=brightData, dynamic_text=dynamic_text)


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
        polGraphDat[3].append(float(f['Ny'][str(i)][0]))
        

    # map data
    
    borough = [requestedborough + " average", requestedborough + " summer average", requestedborough + " winter average", "citywide average"]
    # values are for how high the pollution are. starter is beginning of graph, end is end
    starterVals = [polGraphDat[0][0], polGraphDat[1][0], polGraphDat[2][0], polGraphDat[3][0]]
    endVals = [polGraphDat[0][13], polGraphDat[1][13], polGraphDat[2][13], polGraphDat[3][13]]
    zDatStart = list(sorted(list(zip(starterVals, borough))))
    zDatEnd = list(sorted(list(zip(endVals, borough))))
    print(zDatStart)
    print(zDatEnd)
    # this creates a list of tuples that we will use to do the text generation
    dynamic_text = 'In 2009, ' + zDatStart[3][1] + " had a " + giveSeverity115(zDatStart[3][0]) + " pollution level, and was the highest metric. "
    dynamic_text = dynamic_text + zDatStart[2][1] + " and " + zDatStart[1][1] + " followed, with a " + giveSeverity115(zDatStart[2][0]) + " and " + giveSeverity115(zDatStart[1][0]) + " level of pollution."
    dynamic_text = dynamic_text + zDatStart[0][1] + " had the lowest pollution."
   
    dynamic_text = 'In 2023, ' + zDatEnd[3][1] + " had a " + giveSeverity115(zDatEnd[3][0]) + " pollution level, and was the highest metric. "
    dynamic_text = dynamic_text + zDatEnd[2][1] + " and " + zDatEnd[1][1] + " followed, with a " + giveSeverity115(zDatEnd[2][0]) + " and " + giveSeverity115(zDatEnd[1][0]) + " level of pollution."
    dynamic_text = dynamic_text + zDatEnd[0][1] + " had the lowest pollution."
    return render_template('micro.html', borough=requestedborough, endpoints=polGraphDat, dynamic_text=dynamic_text)



app.run(debug=True, port=25565)
