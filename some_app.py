import os
from io import BytesIO
import base64
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
app.config['RECAPTCHA_USE_SSL'] = True
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
    image_string=None
    origin_platname_string=None
    rgb=None
    image_modifi_string=None
    modifi_platname_string=None
    files_info=None

    if form.validate_on_submit():
        image = Image.open(BytesIO(form.upload.data.read()))
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        image_string = base64.b64encode(buffered.getvalue())
        image_string = image_string.decode('utf-8')
        width, height = image.size
        scale = form.scale.data
        width_modifi, height_modifi = int(width*scale), int(height*scale)
        image_modifi = image.resize((width_modifi, height_modifi))
        buffered_modifi = BytesIO()
        image_modifi.save(buffered_modifi, format="JPEG")
        image_modifi_string = base64.b64encode(buffered_modifi.getvalue())
        image_modifi_string = image_modifi_string.decode('utf-8')

        fig1, ax1 = plt.subplots()
        rgb = image.split()
        x = range(256)
        ry = rgb[0].histogram()
        gy = rgb[1].histogram()
        by = rgb[2].histogram()
        ax1.plot(x, ry, color='r')
        ax1.plot(x, gy, color='g')
        ax1.plot(x, by, color='b')
        buffered_origin_platname = BytesIO()
        fig1.savefig(buffered_origin_platname, format="JPEG")
        origin_platname_string = base64.b64encode(buffered_origin_platname.getvalue())
        origin_platname_string = origin_platname_string.decode('utf-8')

        fig2, ax2 = plt.subplots()
        rgb = image_modifi.split()
        x = range(256)
        ry = rgb[0].histogram()
        gy = rgb[1].histogram()
        by = rgb[2].histogram()
        ax2.plot(x, ry, color='r')
        ax2.plot(x, gy, color='g')
        ax2.plot(x, by, color='b')
        buffered_modifi_platname = BytesIO()
        fig2.savefig(buffered_modifi_platname, format="JPEG")
        modifi_platname_string = base64.b64encode(buffered_modifi_platname.getvalue())
        modifi_platname_string = modifi_platname_string.decode('utf-8')

        files_info = {
            'filename_origin': image_string,
            'origin_size': f"{width}x{height}",
            'origin_platname': origin_platname_string,
            'filename_modifi': image_modifi_string,
            'modifi_size': f"{width_modifi}x{height_modifi}",
            'modify_plotname': modifi_platname_string
        }
    return render_template('simple.html',form=form,files_info=files_info) 