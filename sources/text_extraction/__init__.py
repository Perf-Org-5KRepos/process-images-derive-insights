from flask import Flask, redirect, render_template, request
import os
import sys
from PIL import Image
import pytesseract
import argparse
from flasgger import Swagger
from server import app
from server.routes.prometheus import track_requests

app=Flask(__name__)
UPLOAD_FOLDER = './userapp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# The python-flask stack includes the flask extension flasgger, which will build
# and publish your swagger ui and specification at the /apidocs url. Here we set up
# the basic swagger attributes, which you should modify to match you application.
# See: https://github.com/rochacbruno-archive/flasgger
swagger_template = {
  "swagger": "2.0",
  "info": {
    "title": "Example API for python-flask stack",
    "description": "API for helloworld, plus health/monitoring",
    "contact": {
      "responsibleOrganization": "IBM",
      "responsibleDeveloper": "Henry Nash",
      "email": "henry.nash@uk.ibm.com",
      "url": "https://appsody.dev",
    },
    "version": "0.2"
  },
  "schemes": [
    "http"
  ],
}
swagger = Swagger(app, template=swagger_template)

# The python-flask stack includes the prometheus metrics engine. You can ensure your endpoints
# are included in these metrics by enclosing them in the @track_requests wrapper.
@app.route('/hello')
@track_requests
def HelloWorld():
    # To include an endpoint in the swagger ui and specification, we include a docstring that
    # defines the attributes of this endpoint.
    """A hello message
    Example endpoint returning a hello message
    ---
    responses:
      200:
        description: A successful reply
        examples:
          text/plain: Hello from Appsody!
    """
    return 'Your text extraction application test is successful'

@app.route("/home")
def home():
  return "Your text extraction application test is successful"

@app.route('/extract', methods = ['GET', 'POST'])
@track_requests
def text_extraction():
   if request.method == 'POST':
      f = request.files['file']

      # create a secure filename
      filename = f.filename

      # save file 
      filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
      f.save(filepath)

      # perform OCR on the processed image with HINDI text
      text = pytesseract.image_to_string(Image.open(filepath),lang = 'hin')

      return text

# It is considered bad form to return an error for '/', so let's redirect to the apidocs
@app.route('/')
def index():
    return redirect('/apidocs')

# If you have additional modules that contain your API endpoints, for instance
# using Blueprints, then ensure that you use relative imports, e.g.:
# from .mymodule import myblueprint
