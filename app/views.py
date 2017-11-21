from flask import render_template, jsonify, redirect, url_for, request
from app import app, rpc

@app.route('/')
def home():
	info = rpc.getinfo()

	return render_template('home.html', info=info)