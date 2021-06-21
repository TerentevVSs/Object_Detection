from flask import request, render_template, flash, redirect, \
    url_for, send_from_directory
from forms import LoginForm
from app import app
import os
from werkzeug.utils import secure_filename
import model
import wget


@app.route('/')
def home():
    user = {'username': 'Anonymous',
            "IP": request.remote_addr,
            "browser": request.user_agent
            }
    return render_template('Home.html', title='Home', user=user)



#Предполгалось сделать возможность регистрации и сохранения своих фото,
#однако это оказалось нетривиальной задачей..
#@app.route('/Log In/', methods=["GET", "POST"])
#def login():
#    form = LoginForm()
#    if form.validate_on_submit():
#        # flash("Login requested for user {}, remember_me={}"
#        #      .format(form.username.data, form.remember_me.data))
#        return redirect(url_for('home'))
#    return render_template('Login.html', title='Sign In', form=form)



UPLOAD_FOLDER = './app/static/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/Upload/', methods=['GET', 'POST'])
def upload():
    user = {'username': 'Anonymous',
            "IP": request.remote_addr,
            "browser": request.user_agent
            }
    uploaded = 0
    if request.method == 'POST':
        file = request.files['file']
        uploaded = 0
        if file and (file.content_type.rsplit('/', 1)[
                         1] in ALLOWED_EXTENSIONS).__bool__():
            filename = secure_filename(file.filename)
            file.save(
                os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded = 1
        else:
            uploaded = -1
    if uploaded == 1:
        boxed = model.look_image(filename)
        return render_template("Upload.html",
                               title='Upload',
                               uploaded="Success. "
                                        "Your file was uploaded.",
                               user=user,
                               image=filename,
                               boxed_image=boxed
                               )
    if uploaded == -1:
        return render_template("Upload.html",
                               title='Upload',
                               uploaded="Incorrect format of file. "
                                        "We are working only with "
                                        "png, jpg, jpeg.",
                               user=user)

    return render_template("Upload.html",
                           title='Upload',
                           uploaded="", user=user)


@app.route("/Link/", methods=['GET', 'POST'])
def link():
    user = {'username': 'Anonymous',
            "IP": request.remote_addr,
            "browser": request.user_agent
            }
    uploaded = 0
    if request.method == 'POST':
        uploaded = 0
        link = request.get_data(as_text=True)
        url = link[link.find('http'):link.rfind('.') + 5]
        if url[-1]!='g':
            url=url[:-1]
        wget.download(url, UPLOAD_FOLDER + "test1.jpg")
        filename = url.split('/')[len(url.split('/'))-1]
        ext = url.split('.')[len(url.split('.'))-1]
        if (ext in ALLOWED_EXTENSIONS).__bool__():
            wget.download(url, UPLOAD_FOLDER + filename)
            uploaded = 1
        else:
            uploaded = -1

    if uploaded == 1:
        boxed = model.look_image(filename)
        return render_template("Link.html",
                               title='Link',
                               uploaded="Success. "
                                        "Your file was uploaded.",
                               user=user,
                               image=filename,
                               boxed_image=boxed
                               )
    if uploaded == -1:
        return render_template("Link.html",
                               title='Link',
                               uploaded="Incorrect format of file. "
                                        "We are working only with "
                                        "png, jpg, jpeg.",
                               user=user)

    return render_template("Link.html",
                           title='Link',
                           uploaded="", user=user)
