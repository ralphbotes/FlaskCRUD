from functions.database_functions import *
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route("/")
@app.route("/index")
def home():
    db_creation_msg = create_db()
    return render_template('index.html', msg = db_creation_msg)

@app.route('/new_driver')
def new_driver():
    return render_template('addnew.html')

@app.route('/add_to_db',methods = ['POST', 'GET'])
def add_to_db():
    db_addition_msg = add_new()
    return render_template("index.html", msg = db_addition_msg)

@app.route('/list')
def list():
   rows = list_db()
   return render_template("list.html",rows = rows)

@app.route('/remove/<id>')
def remove(id):
    user = user_selected(id)
    return render_template("remove.html", user = user)

@app.route('/remove_selected/<id>')
def remove_selected(id):
    delete_driver(id)
    return redirect(url_for('list'))

@app.route('/update/<id>')
def update(id):
    user = user_selected(id)
    return render_template("update.html", user = user)

@app.route('/update_selected',methods = ['POST', 'GET'])
def update_selected():
    update_driver()
    return redirect(url_for('list'))

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)