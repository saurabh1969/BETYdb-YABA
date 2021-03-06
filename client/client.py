#################
#### imports ####
#################

import requests
from flask import Flask, g, render_template,request,redirect,Response,flash,jsonify, make_response
import json
from time import sleep

# Create app
app = Flask(__name__)
app.secret_key = 'my unobvious secret key'

# The maximum allowed payload to 16 megabytes.
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS = set(['csv', 'xls','xlsx'])

@app.route("/")
def index():    
    return render_template("index.html")

@app.route('/experiments',methods = ['POST'])
def experiments():    
    if request.method == 'POST':
        response=postRequest_With_UserName(request,'experiments')
        return Response(response.text,mimetype="application/json")

        
@app.route('/treatments',methods = ['POST'])
def treatments():    
    if request.method == 'POST':
        response=postRequest_With_UserName(request,'treatments')
        return Response(response.text,mimetype="application/json")

@app.route('/cultivars',methods = ['POST'])
def cultivars():    
    if request.method == 'POST':
        response=postRequest(request,'cultivars')
        return Response(response.text,mimetype="application/json") 

@app.route('/citations',methods = ['POST'])
def citations():    
    if request.method == 'POST':
        response=postRequest_With_UserName(request,'citations')
        return Response(response.text,mimetype="application/json") 

@app.route('/experiments_sites',methods = ['POST'])
def experiments_sites():    
    if request.method == 'POST':
        resposne=postRequest(request,'experiments_sites')
        return Response(response.text,mimetype="application/json")  

@app.route('/experiments_treatments',methods = ['POST'])
def experiments_treatments():    
    if request.method == 'POST':
        response=postRequest(request,'experiments_treatments')
        return Response(response.text,mimetype="application/json") 

@app.route('/sites_cultivars',methods = ['POST'])
def sites_cultivars():    
    if request.method == 'POST':
        respose=postRequest(request,'sites_cultivars')
        return Response(response.text,mimetype="application/json") 

@app.route('/citations_sites',methods = ['POST'])
def citations_sites():    
    if request.method == 'POST':
        response=postRequest(request,'citations_sites')
        return Response(response.text,mimetype="application/json") 

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def _url(path):
    return 'http://yaba_api:5000/yaba/v1/' + path

def postRequest(request,endpoint):
    if 'fileName' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['fileName']
    if not file.filename:
        flash('No file selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        payload = {'fileName':file}
        headers = {'content-type': 'application/json'}
        flash('File successfully uploaded')
        sleep(2)
        response = requests.post(_url(endpoint),files=payload)
        return response
            
    else:
        flash('Allowed file types are csv, xls, xlsx')
        return redirect(request.url)

def postRequest_With_UserName(request,endpoint):
    if 'fileName' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['fileName']
    if not file.filename:
        flash('No file selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        username=request.args['username']
        payload = {'fileName':file}
        params={'username':username}
        headers = {'content-type': 'application/json'}
        flash('File successfully uploaded')
        sleep(2)
        response = requests.post(_url(endpoint),files=payload,params=params)
        return response
            
    else:
        flash('Allowed file types are csv, xls, xlsx')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=6000,debug=True,processes=2)

