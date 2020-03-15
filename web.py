
from flask import Flask, render_template, url_for, request, flash, redirect,send_from_directory, send_file, after_this_request
import os
from werkzeug.utils import secure_filename
import MyWebTools as MWT

try:
    os.mkdir('input_folder')  # make the directory to store all the new files
except:
    print('Failed to create input directory')  # if the directory already exist
    print('Probably it already exist')
try:
    os.mkdir('output_folder')  # make the directory to store all the new files
except:
    print('Failed to create output directory')  # if the directory already exist
    print('Probably it already exist')


UPLOAD_FOLDER =os.path.join(os.path.dirname(os.path.abspath(__file__)),'input_folder')
DOWNLOAD_FOLDER=os.path.join(os.path.dirname(os.path.abspath(__file__)),'output_folder')
ALLOWED_EXTENSIONS_FASTQ = {'fastq'}
ALLOWED_EXTENSIONS_FASTA={'fasta','fna','fa'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER']=DOWNLOAD_FOLDER
app.secret_key='hdsgfhdgashjfgjasdk'

def allowed_file(filename, fasta=True): # Check if the extension is correct
    if not fasta:
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_FASTQ
    if fasta:
        return '.' in filename and \
                   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_FASTA


@app.route('/')
@app.route('/output_folder')

@app.route('/home')
def home():
    return render_template('Home.html', title="Home Page")

@app.route('/tools')
def tools():
    return render_template('tools.html')



@app.route('/tools/fastqToFasta', methods=['GET','POST'])

# this page will get the file, process, and send back to user, also will delete the inoput and outpout files inmediately after

def Fastq_to_Fasta():
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
        if file and allowed_file(file.filename, fasta=False):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return process_fastq(filename)  # Process the file and remove after posting
        else:
            return render_template('ErrorPage.html')

    return render_template('fastqToFasta.html')


def process_fastq(filename):
    '''
    This function processes the file and sends the user the processed file, after that deletes both the input file and
    output file
    '''
    processed_filename = filename.rsplit('.', 1)[0] + '.fasta'  # Rename the processed file
    MWT.fastq_to_fasta(os.path.join(app.config['UPLOAD_FOLDER'], filename) # Process the file and output in the
                       , os.path.join(app.config['DOWNLOAD_FOLDER'], processed_filename))# downloads folder

    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename=processed_filename, as_attachment=True),\
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename)), \
            os.remove(os.path.join(app.config['DOWNLOAD_FOLDER'], processed_filename))


@app.route('/tools/Nplots/', methods=['GET','POST'])# form page
def Nplots():
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
        if file and allowed_file(file.filename, fasta=True):
            filename = secure_filename(file.filename)
            window_dim=request.form.getlist('quantity') # get a list with the window dimensions, this returns a string
            window_dim=list(map(int,window_dim))
            plots=request.form.getlist('plot') # get a list with 1 and 0 for the plots
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            plot_fasta(filename, window_values=window_dim, type=plots)
            return redirect('results'), os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #go to the results page and remove the inpu tfile
        else:
            return render_template('ErrorPage.html')

    return render_template('Nplots.html')



def plot_fasta(filename, window_values, type):
    '''
    This function takes the input from the form and sends it to th eplotting function to generate the graphs
    :param filename: Original Filename
    :param window_values: Windoe step and size
    :param type: which plot the user wants, AllN/GC
    :return: the plotting function saves the files in the downlod folder
    '''
    for graph_type in type:
        if graph_type=='gc':
           MWT.plot_nucleotides(fastasequence=os.path.join(app.config['UPLOAD_FOLDER'], filename),\
                    filename=filename, windowsize=window_values[0], step=window_values[1],\
                    GC=True, out_dir_name=app.config['DOWNLOAD_FOLDER'])

        else:
           MWT.plot_nucleotides(fastasequence=os.path.join(app.config['UPLOAD_FOLDER'], filename), \
                                 filename=filename, windowsize=window_values[0], step=window_values[1], \
                                 GC=False, out_dir_name=app.config['DOWNLOAD_FOLDER'])



@app.route('/results/<filename>')#This route will serve the images to the results page
def send_image(filename):
    send_file(app.config['DOWNLOAD_FOLDER'] + filename, mimetype='image/png')



@app.route('/tools/Nplots/results')#Render the page and clean
def show_graphs():
    img_list=os.listdir(app.config['DOWNLOAD_FOLDER'])
    return  render_template('plot_show.html',image_names=img_list), clean(img_list)
def clean(file_list):
    for file in file_list:
        os.remove(os.path.join(app.config['DOWNLOAD_FOLDER'],file))


@app.route('/tools/MultilineFasta', methods=['GET','POST'])
def MultilineFasta():
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
        if file and allowed_file(file.filename, fasta=True):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return process_multiline_fasta(filename) #Process the file and remove after posting
        else:
            return render_template('ErrorPage.html')

    return render_template('MultilineFasta.html')


def process_multiline_fasta(filename):
    '''
    This function processes the file and sends the user the processed file (one line fasta), after that deletes both the
    input file and output file
    '''
    processed_filename = filename.rsplit('.', 1)[0] + '_oneline.fasta'  # Rename the processed file
    MWT.oneline_fasta(os.path.join(app.config['UPLOAD_FOLDER'], filename) # Process the file and output in the
                       , os.path.join(app.config['DOWNLOAD_FOLDER'], processed_filename))# downloads folder

    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename=processed_filename, as_attachment=True),\
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename)), \
            os.remove(os.path.join(app.config['DOWNLOAD_FOLDER'], processed_filename))



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