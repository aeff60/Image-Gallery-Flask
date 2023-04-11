from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfadsf'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', 'POST'])
def UploadFile2Web ():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

    image_files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', form=form, image_files=image_files)

if __name__ == '__main__':
    app.run(debug=True)
