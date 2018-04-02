from flask import render_template, redirect, url_for, request
from time import time
from chinchilla import app, blocksDB, txDB
from pymongo import DESCENDING

@app.route('/')
def home():
	try:
		now = int(time())
		if request.args.get('page'):
			page = int(request.args.get('page'))
		else:
			page = 1

		blockCount = blocksDB.count()

		maxPage = int((blockCount - 19)/20)
		delta = blockCount - page*20

		pages = {'current' : page, 'max' : maxPage + 2}

		blockArray = blocksDB.find({'height' : {'$gte' : delta, '$lt' : delta + 20}}).sort('height', DESCENDING).limit(20)

		return render_template('home.html', blocks=blockArray, pages=pages, now=now)
	except:
		return render_template('error.html')
		
@app.route('/block/<string:hash>')
def block(hash):
	try:
		blockInfo = blocksDB.find_one({ 'hash' : hash })
		height = blockInfo['height']

		txArray = []
		tx_query = txDB.find({ 'hash' : {'$in' : blockInfo['tx'] } })

		for tx in tx_query:
			print(tx)
			amount = 0
			for j in tx['vout']:
				amount += float(j['value'])

			txDict = {'hash' : tx['txid'],
					'inputs' : len(tx['vin']),
					'outputs' : len(tx['vout']), 
					'amount' : '{0:.8f}'.format(amount),
					'size' : tx['size']}
			
			txArray.append(txDict)

		return render_template('block.html', tx=txArray, height=height)
	except:
		return render_template('error.html')


@app.route('/tx/<string:txid>')
def tx(txid):
	try:
		tx = txDB.find_one({ 'txid' : txid})

		vin = []
		vout = []

		inputvalue = 0.0
		outputvalue = 0.0

		for j in tx['vout']:
			if j['scriptPubKey']['type'] == 'pubkeyhash' or j['scriptPubKey']['type'] == 'pubkey':

				addresses = j['scriptPubKey']['addresses'][0]
				value = float(j['value'])
				vout.append({'value' : '{0:.8f}'.format(value), 'addresses' : addresses})
				
				outputvalue += value

		if len(tx['vin']) == 1 and not 'vout' in tx['vin'][0]:
			vin.append({'value' : 'Generación de Chauchas', 'addresses' : 'Generación de Chauchas'})

		else:
			addr = []

			txid_array = [i['txid'] for i in tx['vin']]
			txvin = [{'n' : i['vout'], 'txid' : i['txid'] } for i in tx['vin']]
			query = txDB.find({ 'txid' : {'$in' : txid_array }})

			for i in query:

				for j in txvin:
					if i['txid'] == j['txid']:
						n = j['n']

				addresses = i['vout'][n]['scriptPubKey']['addresses'][0]
				value = float(i['vout'][n]['value'])
				vin.append({'value' : '{0:.8f}'.format(value), 'addresses' : addresses, 'txid' : i['txid']})

				inputvalue += value

		return render_template('tx.html', vout=vout, vin=vin, txid=txid, fee=(inputvalue - outputvalue))
	except:
		return render_template('error.html')
