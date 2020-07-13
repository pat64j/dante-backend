from flask import render_template
from . import index

@index.route('/')
def home():
    return render_template('index.html')
