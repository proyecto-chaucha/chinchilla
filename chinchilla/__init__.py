from flask import Flask

app = Flask(__name__)

# python -c "import os; print(repr(os.urandom(32)));"
app.config['SECRET_KEY'] = b'una clave bien larga y random'

from chinchilla import views