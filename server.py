# flask --app data_server run
from flask import Flask
from flask import request
from flask import render_template
import json

f = open("data/formatted_aq.json", "r")
f = json.load(f)

app = Flask(__name__, static_url_path='', static_folder='static')

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
    if requestedYear == 'None':
        print("request average!")
        requestedYear = "NYC average from year-year"
    print(requestedYear)
    return render_template('index.html', all_borough=all_boroughs, all_years=all_years, requestedYear=requestedYear)


@app.route('/about')
def about():
    # so for macro we will do a map with the average data for each borough
    # and for the micro we will have a graph with summer vs winter vs avg vs avg for rest of city
    return render_template('about.html')

@app.route('/borough')
def borough():
    requestedborough = request.args.get('borough')
    return render_template('micro.html', borough=requestedborough, endpoints=[[1, 100, 212],[],[],[]])



app.run(debug=True, port=25565)
