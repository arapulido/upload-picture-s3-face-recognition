# IMPORTS
from ddtrace import patch_all, config
patch_all(logging=True)
config.flask['service_name'] = 'face_recognition_app'

from flask import Flask, render_template, request

from werkzeug.utils import secure_filename
import json
import os
import requests
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
from tools import upload_file_to_s3

# CONFIG
application = Flask(__name__, instance_relative_config=True)
application.config.from_object(os.environ['APP_SETTINGS'])

# Logger
file_handler = RotatingFileHandler(os.environ['APP_LOGS'] + 'face_recognition.log', maxBytes=10000, backupCount=1)
FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')
file_handler.setFormatter(Formatter(FORMAT))
application.logger.addHandler(file_handler)
application.logger.setLevel(logging.DEBUG)

ALLOWED_EXTENSIONS = application.config["ALLOWED_EXTENSIONS"]


# ROUTES
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # There is no file selected to upload
        if "user_file" not in request.files:
            return "No user_file key in request.files"

        if request.form['user_id'] == None:
            return "Please, add a user name"

        user_name = request.form['user_id']

        file = request.files["user_file"]

        # There is no file selected to upload
        if file.filename == "":
            return "Please select a file"

        # File is selected, upload to S3 and show S3 URL
        if file and allowed_file(file.filename):

            data = {"srcBucket": application.config['S3_BUCKET'],
            "name":file.filename, 
            "userId": user_name} 

            file.filename = secure_filename(file.filename)
            application.logger.info("Uploading %s file to %s bucket", file.filename, application.config['S3_BUCKET'])
            upload_success = upload_file_to_s3(file, application.config['S3_BUCKET'], application.config['S3_KEY'], application.config['S3_SECRET'])

            if upload_success != True:
                return "Error uploading to S3"

            return requests.post(application.config['FACE_DETECTION_ENDPOINT'],
                data=json.dumps(data)).content
    else:
        return render_template("index.html")


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
