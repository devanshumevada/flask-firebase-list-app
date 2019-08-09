from flask import Flask, request, render_template, url_for, redirect
import pyrebase

config = {
    "apiKey": "AIzaSyBqa5GKJfK8ZjsOQGp4ZnT2HIFsr1VBq0s",
    "authDomain": "notes-35255.firebaseapp.com",
    "databaseURL": "https://notes-35255.firebaseio.com",
    "projectId": "notes-35255",
    "storageBucket": "notes-35255.appspot.com",
    "messagingSenderId": "706848575692",
    "appId": "1:706848575692:web:333fa0dd533b89d9"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
app = Flask(__name__)

@app.route('/')
def index():
    empty=True
    all_entries= {}
    all_entries = db.child("entries").get()
    if all_entries.val():
        empty=False
        return render_template('index.html',all_entries=all_entries, empty_dict=empty)
    else:
        return render_template('index.html',empty_dict=empty)

@app.route('/add_item',methods=['POST'])
def add_item():
    title = request.form['title']
    description = request.form['desc']
    if title and description:
        db.child("entries").push({"title":title, "description":description})
    return redirect(url_for('index'))

@app.route('/delete_item/<string:id>',methods=['GET'])
def delete_item(id):
    db.child("entries").child(id).remove()
    return redirect(url_for('index'))

@app.route('/update_item',methods=['POST'])
def update_item():
    id = request.form['uid']
    updated_title = request.form['utitle']
    updated_desc = request.form['udesc']
    if id and updated_title and updated_desc:
        db.child("entries").child(id).update({"title":updated_title, "description":updated_desc})
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)
