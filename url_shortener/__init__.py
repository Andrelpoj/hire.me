from flask import Flask
import markdown 
import os 

app = Flask(__name__)

@app.route("/")
def index():
    """Present API Documentation"""

    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as readme:
        content = readme.read()
        return markdown.markdown(content)