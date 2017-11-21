from flask import render_template, jsonify, redirect, url_for, request
from app import app, rpc

@app.route('/')
def home():
	return str(rpc.getinfo()['blocks'])