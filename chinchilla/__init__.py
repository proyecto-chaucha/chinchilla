from chinchilla.config import RPCuser, RPCpassword, RPCport
from pymongo import MongoClient
from flask import Flask

# MongoDB
client = MongoClient()
db = client['blockchain']

# Collections
blocksDB = db['blocks']
txDB = db['tx']
diffDB = db['diff']

app = Flask(__name__)

# python -c "import os; print(repr(os.urandom(32)));"
app.config['SECRET_KEY'] = b'\xb9\xe3"\xb3,\xf7\xda6t\x16\xccy\xa9\x7f\xeb\x1c"Z\xfe\xc1\xca\xfaYWx\x07\xce\x92N03\xe6'

from chinchilla import views