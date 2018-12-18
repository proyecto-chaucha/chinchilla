from flask import Flask

app = Flask(__name__)

app.config['genesis_tx'] = '1b54ad13e84ece043533beb59d6b666047ffc77a4496034a101791601d711998'

from chinchilla import views