from flask import Flask
from pymongo import MongoClient

app= Flask(__name__)
# app.secret_key= '9c51e42f9311aea588e54c4d'

client =MongoClient()
client =MongoClient("mongodb://localhost:27017/")

db= client['MAss']

if __name__ == '__main__':
    app.run(debug=True)