from os import environ
from chinchilla import app

if __name__ == '__main__':
	HOST = environ.get('SERVER_HOST', 'localhost')
	try:
		PORT = int(environ.get('SERVER_PORT', '8080'))
	except ValueError:
		PORT = 8080
	app.run(HOST, PORT, True, threaded=True)