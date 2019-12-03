from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.Playlister
playlists = db.playlists

app = Flask(__name__)

def video_url_creator(id_lst):
    videos = []
    for vid_id in id_lst:
        # We know that embedded YouTube videos always have this format
        video = 'https://youtube.com/embed/' + vid_id
        videos.append(video)
    return videos

@app.route('/')
def playlists_index():
    """Show all playlists."""
    return render_template('playlists_index.html', playlists=playlists.find())
    
    
@app.route('/playlists/new')
def playlists_new():
    """Create a new playlist."""
    return render_template('playlists_new.html', playlist={}, title='New Playlist')


# Note the methods parameter that explicitly tells the route that this is a POST
@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """Submit a new playlist."""
    # Grab the video IDs and make a list out of them
    video_ids = request.form.get('video_ids').split()
    # call our helper function to create the list of links
    videos = video_url_creator(video_ids)
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'video_ids': video_ids,
        'videos': videos,
        'ratings': int(request.form.get('ratings'))
    }
    playlist_id = playlists.insert_one(playlist).inserted_id
    return redirect(url_for('playlists_show', playlist_id=playlist_id))

@app.route('/playlists/<playlist_id>', methods= ['GET'])
def playlists_show(playlist_id):
    """Show a single playlist."""
    playlist = playlists.find_one({"_id": ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist)

@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    """Show the edit form for a playlist."""
    # Add the title parameter here
    playlist = playlists.find_one({"_id": ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title="Edit Playlist")

@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    """Submit an edited playlist."""
    video_ids = request.form.get('video_ids').split()
    videos = video_url_creator(video_ids)
    # create our updated playlist
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids,
        'ratings': int(request.form.get('ratings'))
    }
    # set the former playlist to the new one we just updated/edited
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    # take us back to the playlist's show page
    return redirect(url_for('playlists_show', playlist_id=playlist_id))

@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    """Delete one playlist."""
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for("playlists_index"))

if __name__ == '__main__':
    app.run(debug=True)
