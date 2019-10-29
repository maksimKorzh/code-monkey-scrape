######################################################
# 
# Libraries
#
######################################################

from flask import Flask
from flask import request
from flask import Response
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
import requests
from bs4 import BeautifulSoup
import json


######################################################
# 
# App instance
#
######################################################

app = Flask(__name__)


######################################################
# 
# Routes
#
######################################################

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scrape')
def scrape():
    #flash(request.args.get('url'), 'success')
    url = request.args.get('url')
    
    try:    
        response = requests.get(url)
        content = BeautifulSoup(response.text, 'lxml').prettify()
    except:
        flash('Failed to retrieve URL "%s"' % url, 'danger')
        content = ''

    return render_template('scrape.html', content=content)

# render results to screen
@app.route('/results')
def results():
    args = []
    results = []
    
    for index in range(0, len(request.args.getlist('tag'))):
        args.append({
            'tag': request.args.getlist('tag')[index],
            'css': request.args.getlist('css')[index],
            'attr': request.args.getlist('attr')[index],
        })
    
    response = requests.get(request.args.get('url'))
    content = BeautifulSoup(response.text, 'lxml')
    
    # item to store scraped results
    item = {}
    
    # loop over request arguments
    for arg in args:
        # store item
        item[arg['css']] = [one.text for one in content.findAll(arg['tag'], arg['css'])]
    
    # loop over row indexes
    for index in range(0, len(item[next(iter(item))])):
        row = {}
        
        # loop over stored data
        for key, value in item.items():
            # append value to the new row
            row[key] = '"' + value[index] + '"'
        
        # append new row to results list
        results.append(row)
    
    return render_template('results.html', results=results)


######################################################
# 
# Run app
#
######################################################

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True, threaded=True)
