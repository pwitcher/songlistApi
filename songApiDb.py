import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Pete's Song List (dB)</h1>
<p>A prototype API for songs Pete knows, powered by a database.</p>'''

@app.route('/api/v1/resources/songs/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('songlist.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_songs = cur.execute('SELECT * FROM songlist;').fetchall()

    return jsonify(all_songs)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>No results match your request.</p>", 404

@app.route('/api/v1/resources/songs/title', methods=['GET'])
def api_title():
    query_parameters = request.args

    title = query_parameters.get('title')

    query = "SELECT * FROM songlist WHERE"
    to_filter = []

    if title:
        query += ' title=? AND'
        to_filter.append(title)
    else:
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('songlist.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

@app.route('/api/v1/resources/songs/artist', methods=['GET'])
def api_artist():
    query_parameters = request.args

    artist = query_parameters.get('artist')

    query = "SELECT * FROM songlist WHERE"
    to_filter = []

    if artist:
        query += ' artist=? AND'
        to_filter.append(artist)
    else:
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('songlist.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

@app.route('/api/v1/resources/songs/genre', methods=['GET'])
def api_genre():
    query_parameters = request.args

    genre = query_parameters.get('genre')

    query = "SELECT * FROM songlist WHERE"
    to_filter = []

    if genre:
        query += ' genre=? AND'
        to_filter.append(genre)
    if not (genre):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('songlist.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

@app.route('/api/v1/resources/songs/decade', methods=['GET'])
def api_decade():
    query_parameters = request.args

    decade = query_parameters.get('decade')

    query = "SELECT * FROM songlist WHERE"
    to_filter = []

    if decade:
        query += ' decade=? AND'
        to_filter.append(decade)
    if not (decade):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('songlist.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()
