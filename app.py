import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)

def dict_factory(cursor, row):
    """
    Standard dictionary factory modified to nest musical metadata.
    This ensures the JSON output matches our OpenAPI Spec.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    
    # NESTING LOGIC: Move key/tempo into a musical_metadata object
    # This happens dynamically as the database rows are processed
    if 'key' in d or 'tempo' in d:
        d['musical_metadata'] = {
            'key': d.pop('key', None),
            'tempo': d.pop('tempo', None)
        }
    return d

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Pete's Songbook API v2.2</h1>
<p>A professional repertoire API with multi-leveled musical metadata.</p>'''

def get_db_results(query, params=()):
    """Helper to handle database connections and clean up properly."""
    conn = sqlite3.connect('songlist.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query, params).fetchall()
    conn.close()
    return results

@app.route('/api/v1/resources/songs/all', methods=['GET'])
def api_all():
    results = get_db_results('SELECT * FROM songlist;')
    return jsonify(results)

@app.route('/api/v1/resources/songs/search', methods=['GET'])
def api_search():
    """Unified search endpoint for filtering by artist, genre, tempo, or key."""
    query_parameters = request.args
    
    artist = query_parameters.get('artist')
    genre = query_parameters.get('genre')
    tempo = query_parameters.get('tempo')
    key = query_parameters.get('key')

    query = "SELECT * FROM songlist WHERE"
    to_filter = []

    if artist:
        query += ' artist=? AND'
        to_filter.append(artist)
    if genre:
        query += ' genre=? AND'
        to_filter.append(genre)
    if tempo:
        query += ' tempo=? AND'
        to_filter.append(tempo)
    if key:
        query += ' key=? AND'
        to_filter.append(key)

    if not (artist or genre or tempo or key):
        return page_not_found(404)

    query = query[:-4] + ';' # Remove the trailing ' AND'
    results = get_db_results(query, to_filter)
    return jsonify(results)

@app.route('/api/v1/resources/songs/title', methods=['GET'])
def api_title():
    title = request.args.get('title')
    if not title:
        return page_not_found(404)
    
    results = get_db_results("SELECT * FROM songlist WHERE title=?;", (title,))
    return jsonify(results)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "No results match your request."}), 404

@app.route('/api/v1/resources/songs/artist', methods=['GET'])
def api_artist():
    artist = request.args.get('artist')
    if not artist:
        return page_not_found(404)
    
    # Query the database for matches matching the artist column
    results = get_db_results("SELECT * FROM songlist WHERE artist=?;", (artist,))
    
    if not results:
        return page_not_found(404)
    return jsonify(results)
        
if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.run()