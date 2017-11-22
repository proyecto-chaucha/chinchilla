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

@app.route('/block/<string:hash>')
def block(hash):
	blockInfo = rpc.getblock(hash)
	height = blockInfo['height']

	txArray = []
	for i in blockInfo['tx']:
		rawTx = rpc.getrawtransaction(i)
		tx = rpc.decoderawtransaction(rawTx)

		txDict = {'hash' : tx['txid'], 'inputs' : len(tx['vin']), 'outputs' : len(tx['vout']) }
		txArray.append(txDict)

	print (txArray)

	return render_template('block.html', tx=txArray, height=height)