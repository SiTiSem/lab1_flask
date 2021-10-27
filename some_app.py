import os
from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import SubmitField, FloatField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_bootstrap import Bootstrap
from PIL import Image
from matplotlib import pyplot as plt
from werkzeug.utils import secure_filename

app = Flask(__name__)
bootstrap = Bootstrap(app)

SECRET_KEY = 'qYlBLlrwjCYFO3LglAxdDSceH36pfYTb'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdJKfgcAAAAAF0MiTTxDxbgA6oh_f6HekM4geWO'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdJKfgcAAAAALDdMV696Jsm2ZqtaM0jAkpqKOhI'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

class NetForm(FlaskForm):
    scale = FloatField('Масштаб', validators = [DataRequired()])
    upload = FileField('Файл загрузки', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображение!')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Отправить')

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = NetForm()
    filename=None
    filename_modifi=None
    rgb=None
    origin_platname=None
    modify_plotname=None
    files_info=None

    if form.validate_on_submit():
        dir_name = './static'
        ext_file = secure_filename(os.path.splitext(form.upload.data.filename)[1])
        filename = dir_name + '/originImg.'+ext_file
        form.upload.data.save(filename)
        image = Image.open(filename)
        width, height = image.size
        scale = form.scale.data
        width_modifi, height_modifi = int(width*scale), int(height*scale)
        image_modifi = image.resize((width_modifi, height_modifi))
        filename_modifi = dir_name+'/modifiImg.'+ext_file
        image_modifi.save(filename_modifi)

        fig1, ax1 = plt.subplots()
        rgb = image.split()
        x = range(256)
        ry = rgb[0].histogram()
        gy = rgb[1].histogram()
        by = rgb[2].histogram()
        ax1.plot(x, ry, color='r')
        ax1.plot(x, gy, color='g')
        ax1.plot(x, by, color='b')
        origin_platname = dir_name+'/originPlot.jpg'
        fig1.savefig(origin_platname)

        fig2, ax2 = plt.subplots()
        rgb = image_modifi.split()
        x = range(256)
        ry = rgb[0].histogram()
        gy = rgb[1].histogram()
        by = rgb[2].histogram()
        ax2.plot(x, ry, color='r')
        ax2.plot(x, gy, color='g')
        ax2.plot(x, by, color='b')
        modify_plotname = dir_name+'/modifyPlot.jpg'
        fig2.savefig(modify_plotname)

        files_info = {
            'filename_origin': filename,
            'origin_size': f"{width}x{height}",
            'origin_platname': origin_platname,
            'filename_modifi': filename_modifi,
            'modifi_size': f"{width_modifi}x{height_modifi}",
            'modify_plotname': modify_plotname
        }
    return render_template('simple.html',form=form,files_info=files_info) 