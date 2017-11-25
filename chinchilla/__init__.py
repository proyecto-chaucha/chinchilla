from flask import Flask
from bitcoinrpc.authproxy import AuthServiceProxy

RPCuser = 'chaucha'
RPCpassword = 'probando'
RPCport = 21662

app = Flask(__name__)

# python -c "import os; print(repr(os.urandom(32)));"
app.config['SECRET_KEY'] = b'\xb9\xe3"\xb3,\xf7\xda6t\x16\xccy\xa9\x7f\xeb\x1c"Z\xfe\xc1\xca\xfaYWx\x07\xce\x92N03\xe6'

rpc = AuthServiceProxy("http://%s:%s@127.0.0.1:%i"%(RPCuser, RPCpassword, RPCport))

from chinchilla import views