from flask import render_template, jsonify, redirect, url_for, request
from app import app, rpc
from time import strftime, localtime

@app.route('/')
def home():
	info = rpc.gettxoutsetinfo()

	blockCount = rpc.getblockcount()
	blockArray = []

	for i in range(blockCount - 20, blockCount + 1):
		blockHash = rpc.getblockhash(i)
		block = rpc.getblock(blockHash)
		block['time'] = strftime("%d %b %Y %H:%M:%S", localtime(block['time']))
		blockArray.append(block)

	return render_template('home.html', blocks=blockArray[::-1], info=info)

@app.route('/block/<string:hash>')
def block(hash):
	info = rpc.gettxoutsetinfo()

	try:
		blockInfo = rpc.getblock(hash)
		height = blockInfo['height']

		txArray = []
		for i in blockInfo['tx']:
			rawTx = rpc.getrawtransaction(i)
			tx = rpc.decoderawtransaction(rawTx)
			amount = 0
			for j in tx['vout']:
				amount += j['value']

			txDict = {'hash' : tx['txid'],
					'inputs' : len(tx['vin']),
					'outputs' : len(tx['vout']), 
					'amount' : float(amount) }
			txArray.append(txDict)

		print (txArray)

		return render_template('block.html', tx=txArray, height=height, info=info)
	except:
		return render_template('error.html', info=info)

@app.route('/tx/<string:txid>')
def tx(txid):
	info = rpc.gettxoutsetinfo()

	try:
		rawTx = rpc.getrawtransaction(txid)
		tx = rpc.decoderawtransaction(rawTx)

		vin = []
		vout = []

		for j in tx['vout']:
			vout.append({'value' : '{0:.8f}'.format(j['value']), 'addresses' : j['scriptPubKey']['addresses']})

		if len(tx['vin']) == 1 and tx['vin'][0]['sequence'] == 0:
			vin.append({'value' : '{0:.8f}'.format(10.0), 'addresses' : ['GENERACIÓN']})

		else:
			for i in tx['vin']:
				rawTx = rpc.getrawtransaction(i['txid'])
				tx = rpc.decoderawtransaction(rawTx)
				n = i['vout']

				print(tx['vout'])

				vin.append({'value' : '{0:.8f}'.format(tx['vout'][n]['value']), 'addresses' : tx['vout'][n]['scriptPubKey']['addresses']})

		return render_template('tx.html', vout=vout, vin=vin, info=info, txid=txid)
	except:
		return render_template('error.html', info=info)