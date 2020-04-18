import os
from flask import Flask
from flask import render_template
from flask import request, redirect
from flask import flash, url_for
import json

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route("/arqui")
def hello():
    return "Hello Arqui! This page is just for you!"

#@app.route("/<name>")
#def hello_name(name):
#    return "Hello " + name
    

@app.route('/upload', methods=['POST'])
def upload_image():
	'''
	title=request.form['title']
	description=request.form['description']
	data = {
		"id": 1,
		"title": title,
		"desc" : description,
		"image_name" : ""
	}	
	with open("stat.json", "r+") as stat_file: 
		stat = json.load(stat_file)
		total_count = stat["count"]
		index = stat["index"]
	
		json_filename = str(index+1) + ".json"
		with open(json_filename, "w") as write_file: 
			json.dump(data, write_file)
		
		stat["count"] = total_count + 1
		stat["index"] = index + 1
		stat_file.seek(0)
		json.dump(stat, stat_file)
	'''
	if 'file' not in request.files:
		flash('No file part')
		return redirect('/')
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed')
		#return render_template('index.html', filename=file.filename)
		#print('display_image filename: ' + filename)
		return redirect('/display/'+file.filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		print('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect('/')

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['email']
    print("The email address is '" + email + "'")
    return redirect('/')

if __name__ == '__main__':
	app.run(port=5002,debug=False)
