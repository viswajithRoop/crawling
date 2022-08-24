
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask("lyrics")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lyrics'
db = SQLAlchemy(app)

class Artists(db.Model):
    __tablename__="artists"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    songs = db.relationship("Songs", back_populates="artist")

    def __repr__(self):
        return f"Songs('{self.name}')"

class Songs(db.Model):
    __tablename__="songs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    lyrics = db.Column(db.String)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    artist = db.relationship("Artists", back_populates="songs")

    def __repr__(self):
        return f"Artists('{self.name}')"

@app.route("/")
def index():
    artists = Artists.query.all()
    formatted = []
    for i in artists:
        target = url_for("artists", artist_id = i.id)
        link = f'<a href="{target}">{i.name}</a>'
        formatted.append(f"<li>{link}</li>")
    return "<ul>" + "".join(formatted) + "</ul>"

@app.route("/artist/<int:artist_id>")
def artists(artist_id):
    songs = Songs.query.filter_by(artist_id = artist_id).all()
    formatted = []
    for i in songs:
        target = url_for("songs",song_id=i.id)
        link = f'<a href="{target}">{i.name}</a>'
        formatted.append(f"<li>{link}</li>")
    return "<ul>" + "".join(formatted) + "</ul>"
    

@app.route("/song/<int:song_id>")
def songs(song_id):
    song = Songs.query.filter_by(id = song_id).first()
    lyrics = song.lyrics.replace("\n","<br>")
    return f"""<h2>{song.name}</h2>
{lyrics}"""