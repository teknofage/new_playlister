from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient()
db = client.Playlister
playlists = db.playlists

app = Flask(__name__)

# @app.route('/')
# def index():
#     """Return homeppage."""
#     return render_template('home.html', msg='Flask is Cool!!')
    
# Our mock arrary of projects
# playlists = [
#     {"title": "Cat Videos", "description": "Cats acting weird"},
#     {"title": '80\'s Music', 'description': "Don\'t stop believing!" }
# ]

@app.route('/')
def playlists_index():
    """Show all playlists."""
    return render_template('playlists_index.html', playlists=playlists.find())
    
if __name__ == '__main__':
    app.run(debug=True)
