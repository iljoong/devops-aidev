#!falsk/bin/python
import json
import os
import time
from subprocess import call
import logging

#from flask import Flask, request, send_from_directory, render_template, redirect, Response
from flask import Flask, request, render_template, Response
import appconfig
from appmodel import FruitsModel

LOGGING_LEVELS = {'critical': logging.CRITICAL,
                  'error': logging.ERROR,
                  'warning': logging.WARNING,
                  'info': logging.INFO,
                  'debug': logging.DEBUG}
# global variables

fruits_model = None
app = Flask(__name__, static_folder="wwwroot")

@app.route('/')
def index():
    return about()

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/ping')
def ping():
    res = {'message':  'hello'}
    return Response(json.dumps(res), mimetype='application/json', status=200)

@app.route('/api/warm')
def warm():
    start_time = time.time()
    fruits_model.load()
        
    res = {'message':  'warmed', 'process_time': time.time()- start_time }
    return Response(json.dumps(res), mimetype='application/json', status=200)

@app.route('/api/diag', methods=['GET'])
def diag():

    try:
        blobacct, blobkey, modelpath = fruits_model.get_diag()

        bkey = None if (blobkey == None) else "{}*********".format(blobkey[0:8])
        diag = { "MODELPATH": modelpath, "BLOBACCT": blobacct, "BLOBKEY": bkey, "BLOBPATH": appconfig.container + "/" + appconfig.datapath}
    except Exception as e:
        logging.error(e)
        return Response(json.dumps({"error": str(e)}), mimetype='application/json', status=500)

    return Response(json.dumps(diag), mimetype='application/json')

@app.route('/api/score', methods=['POST'])
def score():
    try:
        start_time = time.time()
        
        f = request.files['file']
        # save original image
        filepath = os.path.join(appconfig.pixpath, f.filename)
        f.save(filepath)

        _predict, _score = fruits_model.score(filepath)

        res = {'label': _predict, 'score': _score, 'process_time': time.time() - start_time }
        
    except Exception as e:
        logging.error(e)
        return Response(json.dumps({"error": str(e)}), mimetype='application/json', status=500)
    
    return Response(json.dumps(res), mimetype='application/json', status=200)

@app.route('/api/update', methods=['PUT'])
def updatemodel():
    try:
        start_time = time.time()
        body = request.json
        modelfile = body['modelfile'] #int

        # sync latest model from blob storage
        blobpath = appconfig.container + '/' + appconfig.modeldir
        downpath = os.path.abspath(appconfig.localmodeldir)
        modelpath = downpath + '/' + modelfile

        blobacct, blobkey = fruits_model.get_blob()

        if not os.path.exists(downpath):
            os.makedirs(downpath)

        logging.info("blobxfer download --storage-account {}  --storage-account-key {} --remote-path {} --local-path {} --skip-on-lmt-ge --strip-components 100".format(blobacct, blobkey, blobpath, downpath))

        call(["blobxfer", "download", "--storage-account", blobacct, "--storage-account-key", blobkey, "--remote-path", blobpath, "--local-path", appconfig.localmodeldir, 
            "--skip-on-lmt-ge", "--strip-components", "100"])

        logging.info("reloading model...")
        fruits_model.update(modelpath)

    except Exception as e:
            return Response(json.dumps({"error": str(e)}), mimetype='application/json', status=500)

    res = {'message':  'updated', 'process_time': time.time()- start_time }
    return Response(json.dumps(res), mimetype='application/json')

@app.route('/api/upload', methods=['POST'])
def upload_blob():

    try:
        start_time = time.time()
        blobpath = appconfig.container + "/" + appconfig.datapath

        blobacct, blobkey = fruits_model.get_blob()

        call(["blobxfer", "upload", "--storage-account", blobacct, "--storage-account-key", blobkey, 
            "--remote-path", blobpath, "--local-path", appconfig.pixpath, "--skip-on-lmt-ge"])

    except Exception as e:
            return Response(json.dumps({"error": str(e)}), mimetype='application/json', status=500)

    res = {'message':  'uploaded', 'process_time': time.time()- start_time }
    return Response(json.dumps(res), mimetype='application/json')

#@app.before_first_request
#def initialize():

if __name__ == '__main__':

    if not os.path.exists(appconfig.pixpath):
        os.makedirs(appconfig.pixpath)
    modelpath = os.environ.get('MODELPATH')
    modelpath = '/models/fruits.h5' if (modelpath == None) else modelpath
    blobacct = os.environ.get('BLOBACCT')
    blobkey = os.environ.get('BLOBKEY')

    fruits_model = FruitsModel(modelpath, blobacct, blobkey)

    app.run(debug=False, threaded=False, host='0.0.0.0',port=8080)
