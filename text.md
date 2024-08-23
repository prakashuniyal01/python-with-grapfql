Set Up the Virtual Environment

python3 -m venv env
source env/bin/activate


deactivate
source env/bin/activate

Percentage of article read
Code

Cloudinary offers SDKs for many programming languages and frameworks. Even though it also offers an Upload API endpoint for both back-end and front-end code, most developers find the SDKs very helpful. If you’re working with a powerful back-end framework like Python Flask, you’ll be happy to hear that a Python SDK is now available.
This tutorial walks you through the process of building an API to upload images to Cloudinary. You can also upload other file types, including video and even nonmedia files, with the API.

Understanding the Difference Between Back End and Front EndCopy link to this heading
Generally, code that runs on the server is back end, and code that runs on the browser is front end. However, since server code can render HTML, CSS, and JavaScript, which all run on the browser, confusion sometimes results. In the context of the Cloudinary SDKs, the back-end ones can read secret credentials, which should not be shared in the front end. In other words, you must never expose the back-end environment variables in the front end because front-end SDKs cannot hide credentials that are meant to be kept secret. As a solution, you can upload browser code with Cloudinary’s unsigned presets without revealing secret credentials. A better way would be to build a back-end API for secure uploads, keeping your API_SECRET credential hidden. Read on to see how to do that with Cloudinary’s Python SDK and Python Flask or Python Django.

Coding a Flask API to Upload to CloudinaryCopy link to this heading
The Flask framework makes it easy to define routes and their functionalities. To get started, first create a route named /upload, which accepts a POST that contains multipart/form-data. You then package up the image file input into a FormData object in a submit handler and POST it to your own Flask API to call Cloudinary’s Upload API, which is configured with your full set of Cloudinary credentials.

Flask’s request option enables you to get data from the client. When submitting files, such as uploading images, you can call upon request to access them.


from flask import Flask,render_template, request
if request.method == 'POST':
    file_to_upload = request.files['file']
Code language: JavaScript (javascript)
However, if you’re looking to simplify the process of building RESTful web services with Flask, you can utilize the flask_restful module. By creating a new class that inherits from Resource, you can define a post() method that accepts the file as a parameter. The werkzeug.datastructures.FileStorage class can be used to get the file object, which can then be saved to a desired location.

Here’s an example of how you can integrate this approach:

from flask import Flask, request from flask_restful import Resource, Api from werkzeug.datastructures import FileStorage app = Flask(__name__) api = Api(app) class UploadFile(Resource): def post(self): file = request.files['file'] file.save('/uploads/' + file.filename) return 'File uploaded successfully!' api.add_resource(UploadFile, '/upload')
This code creates a new Flask project and an API endpoint that allows users to upload files. The post() method of the UploadFile class accepts the file as a parameter and saves it to the /uploads directory. The return statement provides a success message. To test this code, tools like Postman can be used to send a POST request to the /upload endpoint.

The data retrieved from request.files['file'] is an instance of werkzeug.FileStorage. The object can be handed off to the Python SDK’s Upload function. Flask then wraps Werkzeug, which handles the details of the Web Server Gateway Interface (WSGI).


if file_to_upload:
    upload_result = cloudinary.uploader.upload(file_to_upload)
    app.logger.info(upload_result)
For uploads to Cloudinary, the default resource_type is image. To expand or create a new Flask API, add resource_type: 'video' or resource_type: 'raw' for video or raw files, respectively. Raw refers to nonmedia file formats, including text and JSON.

Finally, upload_result is an object that contains the upload response. To complete the actions of your upload API, return that response to the client, like this:


from flask import jsonify
return jsonify(upload_result)
Code language: JavaScript (javascript)
Below is the complete code of your upload API.


@app.route("/upload", methods=['POST'])
def upload_file():
  app.logger.info('in upload route')

  cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET'))
  upload_result = None
  if request.method == 'POST':
    file_to_upload = request.files['file']
    app.logger.info('%s file_to_upload', file_to_upload)
    if file_to_upload:
      upload_result = cloudinary.uploader.upload(file_to_upload)
      app.logger.info(upload_result)
      return jsonify(upload_result)
Code language: JavaScript (javascript)
Setting Up the Flask AppCopy link to this heading
Next, follow the steps below to build the app.

Set Up the Virtual EnvironmentCopy link to this heading
The command below establishes your virtual environment. This is an important step for encapsulating the libraries you’ll be using in this app.


python3 -m venv env
source env/bin/activate
To deactivate the environment, type:


deactivate
source env/bin/activate

Install FlaskCopy link to this heading
Install Flask with this command:


 pip install Flask

Add a requirements.txt FileCopy link to this heading
Create a requirements.txt file to keep track of all the versioned libraries you need for the app and to facilitate future deployment.


 pip freeze > requirements.txt

 pip install flask-cors python-dotenv cloudinary


 Environment Setup Automation:
 
pip install -r requirements.txt


 <!-- importent links  -->

 #### https://cloudinary.com/blog/creating_an_api_with_python_flask_to_upload_files_to_cloudinary


