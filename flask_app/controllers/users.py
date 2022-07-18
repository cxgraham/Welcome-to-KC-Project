from flask_app import app
from flask import render_template, request, redirect, session, flash, url_for
from flask_app.models import user, comment
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/Users/christiangraham/Desktop/CodingDojo/Projects_and_Algos/Solo_Project_Christian_Graham/flask_app/static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# CREATE 
@app.route('/users/register', methods=['POST'])
def register():
    created_user = user.User.create_user(request.form)
    if created_user:
        return redirect('/')
    return redirect('/users/login')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/users/dashboard/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.referrer)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect('/users/dashboard')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = {
                'avatar': "/static/uploads/"+filename
            }
            user.User.upload_avatar(data)
        return redirect(request.referrer)


# READ
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login_create_user.html')
    registered_user = user.User.login(request.form)
    if registered_user:
        return redirect('/')
    return redirect('/users/login')


@app.route('/users/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('user_dashboard.html', this_user = this_user)

@app.route('/top_five_restaurants')
def top_five_restaurants():
    all_comments = comment.Comment.get_all_comments()
    return render_template('top_five_eat.html', all_comments = all_comments)

@app.route('/top_five_things_to_do')
def top_five_to_do():
    all_comments = comment.Comment.get_all_comments()
    return render_template('top_five_to_do.html', all_comments = all_comments)

@app.route('/top_five_bars')
def top_five_bars():
    all_comments = comment.Comment.get_all_comments()
    return render_template('top_five_bar.html', all_comments = all_comments)


# UPDATE 


# DELETE
@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/')