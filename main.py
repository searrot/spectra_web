from flask import Flask, render_template, url_for, request, redirect, flash
import sqlite3
from werkzeug.utils import secure_filename
import os, time, random


#MAX_FILE_SIZE = 2160 * 1440 + 1
UPLOAD_FOLDER = 'D:/_PROGRAMMING/spectra_web/static/user_images/'
extentions = ['jpg', 'jpeg', 'png', 'webp', 'bmp']

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template("main.html")


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    images = os.listdir('D:/_PROGRAMMING/spectra_web/static/user_images/')
    if request.method == 'POST':
        if request.Form['upload_button'] == 'upload':
            images = os.listdir('D:/_PROGRAMMING/spectra_web/static/user_images/')
            file = request.files["upload"]
            print(str(file))

            if file.filename == "":
                flash('No selected file or name of file is empty.')
                return render_template("profile.html", images=sorted(images))
            
            elif file and file.filename.split('.')[1] in extentions:
                name = len(images)
                path = os.path.join(app.config['UPLOAD_FOLDER'], f"{str(name)}.jpg")
                file.save(path)
            else:
                flash('Wrong extention of file.')

            images = os.listdir('D:/_PROGRAMMING/spectra_web/static/user_images/')
            return render_template("profile.html", images=images)
    elif request.method == 'GET':
        images = os.listdir('D:/_PROGRAMMING/spectra_web/static/user_images/')
        try:
            print(images[0])
            return render_template("profile.html", images=images, random=random)
            # <img class="user_img" src="{{ url_for('static', filename='user_images/random_sth_sth') }}"  />
        except Exception as e:
            print(e)
            return render_template("profile.html", images=images, random=random)
    

if __name__ == "__main__":
    app.run(debug=True)
    #<button class="uploadImage" >Загрузить изображение</button> uploadImage upload_btn