
from flask import Flask, render_template, url_for
#import tools

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('Home.html', title="Home Page")

@app.route('/tools')
def tools():
    return render_template('tools.html')

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