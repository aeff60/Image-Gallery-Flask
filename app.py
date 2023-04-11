from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfadsf'

# Azure Blob Storage configuration
CONNECTION_STRING  = "DefaultEndpointsProtocol=https;AccountName=cloudshell1481016573;AccountKey=xY13o85LUOZgEic1fPM0oIg3pt98VTXwkXMXf9sFouHHqNtTLC/wdhMlHoOdFupmfi6lsr4uUFnd+AStRgxNNw==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "imagegallery"

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', 'POST'])
def UploadFile2Web():
    form = UploadFileForm()
    if form.validate_on_submit():
        # Save file to Azure Blob Storage
        file = form.file.data
        filename = secure_filename(file.filename)
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blob_client = container_client.get_blob_client(filename)
        blob_client.upload_blob(file)

    # List files in Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    image_files = [blob.name for blob in container_client.list_blobs()]

    return render_template('index.html', form=form, image_files=image_files)

if __name__ == '__main__':
    app.run(debug=True)
