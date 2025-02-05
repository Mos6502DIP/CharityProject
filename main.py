from flask import *
import sqlite3
import random
import os

app = Flask(__name__)

app.secret_key = 'National Trust'

app.config['UPLOAD_FOLDER'] = '/static/media/place_images'

## Function Tools

def get_extension(filename):
    return filename.split('.')[-1]

## Functions For database
        
def column_check(table, database, column, data):
    conn = sqlite3.connect(database)
    cursor = conn.cursor() 
    cursor.execute(f"SELECT * FROM {table} WHERE {column} = ?", (data,))
    rows = cursor.fetchall()
    if len(rows) == 0:
        return True
    else:
        return False

## Routing for admin

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        if request.form['Password'] == '1234':
            session['admin'] = True
            return redirect('/admin-tools')
        else:
            return render_template('admin.html', admin=session.get('admin'))
    else:
        return render_template('admin.html', admin=session.get('admin'))

@app.route('/admin-tools', methods=['GET'])
def admin_tools():
    if session.get('admin'):
        return render_template('tools.html', admin=session.get('admin'))
    else:
        return 'Access Denied'
    
@app.route('/admin-logout', methods=['GET'])
def admin_logout():
    if session.get('admin'):
        session.clear()
        return redirect('/')
    else:
        return 'Access Denied'
    
@app.route("/add-place", methods=['POST', 'GET'])
def attraction_adder():
    if session.get('admin'):
        if request.method == 'POST':
            thumbnail = request.files['thumbnail']
            banner = request.files['banner']
            thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], get_extension(thumbnail.filename))
            banner_path = os.path.join(app.config['UPLOAD_FOLDER'], get_extension(banner.filename))
            thumbnail.save(thumbnail_path)
            banner.save(banner_path)
        
            return "Uploaded"
        else: 
            return render_template("add_place.html", admin=session.get('admin'))
            
    else:
        return "Access denied"
    
## General user routing

@app.route('/')
def landing():
    return render_template('landing.html', admin=session.get('admin'))




if __name__ == '__main__':
    app.run(debug=True)
