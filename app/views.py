from flask import render_template, jsonify, redirect, url_for, request
from app import app, rpc
from time import time

@app.route('/')
def home():
	blockCount = rpc.getblockcount()
	blockArray = []

	for i in range(blockCount - 10, blockCount + 1):
		blockHash = rpc.getblockhash(i)
		block = rpc.getblock(blockHash)
		block['now'] = time()
		blockArray.append(block)

	return render_template('home.html', blocks=blockArray[::-1])