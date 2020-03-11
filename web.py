
from flask import Flask, render_template, url_for, request, flash, redirect
import os
from werkzeug.utils import secure_filename
import MyWebTools


UPLOAD_FOLDER ='/mnt/e/Pycharm_projects/WebApp/input'
DOWNLOAD_FOLDER='resultado'
ALLOWED_EXTENSIONS_FASTQ = {'fastq'}
ALLOWED_EXTENSIONS_FASTA={'fasta','fna','fa'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER']=DOWNLOAD_FOLDER
app.secret_key='hdsgfhdgashjfgjasdk'

def allowed_file(filename, type='FASTQ'): # Check if the extension is correct
    if type == 'FASTQ':
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_FASTQ
    if type =='FASTA':
        return '.' in filename and \
                   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_FASTA

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_FASTQ

@app.route('/')
@app.route('/home')
def home():
    return render_template('Home.html', title="Home Page")

@app.route('/tools')
def tools():
    return render_template('tools.html')



@app.route('/tools/fastqToFasta/', methods=['GET','POST'])

# def fastqToFasta():
#     return render_template('fastqToFasta.html')

def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect(url_for('upload_file', filename=filename))
    return render_template('fastqToFasta.html')


@app.route('/tools/Nplots/', methods=['GET','POST'])

def Nplots():
    return render_template('Nplots.html')






@app.route('/tools/MultilineFasta/', methods=['GET','POST'])

def MultilineFasta():
    return render_template('MultilineFasta.html')
















@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/references')
def references():
    return render_template('references.html')

if __name__ == '__main__':
    app.run(debug=True)