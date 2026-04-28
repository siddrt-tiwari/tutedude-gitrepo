from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

# Existing DB & collection
db = client["test_db"]
collection = db["users"]
todo_collection = db["todo_items"]


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')

    try:
        if not name or not email:
            raise ValueError("Name and Email are required")

        if collection.find_one({"email": email}):
            raise ValueError("Email already exists")

        collection.insert_one({
            "name": name,
            "email": email
        })

        return redirect(url_for('success'))

    except Exception as e:
        return render_template('form.html', error=str(e), name=name, email=email)


@app.route('/todo')
def todo():
    return render_template('feature-development.html')


@app.route('/submittodoitem', methods=['POST'])
def submit_todo():
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')
    item_id = request.form.get('itemId')
    item_uuid = request.form.get('itemUUID')

    try:
        if not item_name or not item_description or not item_id or not item_uuid:
            raise ValueError("All fields are required")

        todo_collection.insert_one({
            "itemId": item_id,
            "itemName": item_name,
            "itemDescription": item_description
            "itemUUID": item_uuid
        })

        return redirect(url_for('success'))

    except Exception as e:
        return render_template(
            'feature-development.html',
            error=str(e),
            itemName=item_name,
            itemDescription=item_description
        )


@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)