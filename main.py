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
    
def add_place(name, type, description, adult_price, child_price, facilities, thumbnail_name, banner_name):
    connection = sqlite3.Connection('places.db')
    cursor =  connection.cursor()
    cursor.execute("INSERT INTO Places (name, type, description, thumbnail_name, banner_name, adult_price, child_price, facilities) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", 
    (name, type, description, thumbnail_name, banner_name, adult_price, child_price, facilities))

    connection.commit()
    return True

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
            name = request.form['name']
            type = request.form['type']
            description = request.form['description']
            adult_price = request.form['adult-price']
            child_price = request.form['child-price']

            facilities = {}

            if request.form.get("wheelz") == "on":
                facilities['Disabilities'] = {
                    'friendly' : True,
                    'description' : request.form['description-wheelchairs']
                }
            else:
                facilities['Disabilities'] = {
                    'friendly' : False,
                    'description' : request.form['description-wheelchairs']
                }
                
            if request.form.get("cafe") == "on":
                facilities['Cafe'] = True
            else:
                facilities['Cafe'] = False

            if request.form.get("shop") == "on":
                facilities['Shop'] = True
            else:
                facilities['Shop'] = False

            if request.form.get("toilet") == "on":
                facilities['Toilet'] = True
            else:
                facilities['Toilet'] = False
            

            thumbnail = request.files['thumbnail']
            banner = request.files['banner']

            thumbnail_name = f"thumbnail_{name}.{get_extension(thumbnail.filename)}"
            banner_name  = f"banner_{name}.{get_extension(banner.filename)}"
            thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], thumbnail_name)
            banner_path = os.path.join(app.config['UPLOAD_FOLDER'], banner_name)
            thumbnail.save(thumbnail_path)
            banner.save(banner_path)

            if add_place(name, type, description, adult_price, child_price, facilities, thumbnail_name, banner_name):
                return render_template("add_place.html", admin=session.get('admin'))
            else:
                return '505 Error something went wrong.'
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
