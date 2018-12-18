from flask import render_template, redirect, url_for, request
from chinchilla import app
from time import time
from requests import get
from time import strftime, localtime

@app.route('/')
def home():
	if request.args.get('page'):
		page = int(request.args.get('page'))
	else:
		page = 1

	getinfo = get('http://localhost:21662/rest/chaininfo.json').json()
	blockCount = getinfo['blocks']

	maxPage = int((blockCount - 19)/20)
	delta = blockCount - page*20
	
	blockArray = []

	for i in reversed(range(delta + 1, delta + 20 + 1)):
		if i >= 0:
			blockhash = get('http://localhost:21662/rest/getblockhash/' + str(i) + '.json').json()
			block = get('http://localhost:21662/rest/block/' + blockhash + '.json').json()
			block['time'] = strftime('%d.%m.%Y %H:%M:%S', localtime(int(block['time'])))
			blockArray.append(block)
		else:
			break

	pages = {'current' : page, 'max' : maxPage + 2}

	return render_template('home.html', blocks=blockArray, pages=pages)

@app.route('/block/<string:hash>')
def block(hash):
	blockInfo = get('http://localhost:21662/rest/block/' + hash + '.json').json()
	txs = blockInfo['tx']

	txArray = []
	
	for tx in txs:
		amount = 0
		for j in tx['vout']:
			amount += float(j['value'])

		txDict = {'hash' : tx['txid'],
				'inputs' : len(tx['vin']),
				'outputs' : len(tx['vout']), 
				'amount' : '{0:.8f}'.format(amount),
				'size' : tx['size']}
		
		txArray.append(txDict)

	return render_template('block.html', tx=txArray, height=blockInfo['height'])


@app.route('/tx/<string:txid>')
def tx(txid):
	if not txid == app.config['genesis_tx']:
		tx = get('http://localhost:21662/rest/tx/' + txid + '.json').json()

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

			for i in txid_array:
				utxo = get('http://localhost:21662/rest/tx/' + i + '.json').json()

				for j in txvin:
					if utxo['txid'] == j['txid']:
						n = j['n']

				addresses = utxo['vout'][n]['scriptPubKey']['addresses'][0]
				value = float(utxo['vout'][n]['value'])
				vin.append({'value' : '{0:.8f}'.format(value), 'addresses' : addresses, 'txid' : utxo['txid']})

				inputvalue += value
		return render_template('tx.html', vout=vout, vin=vin, txid=txid, fee=(inputvalue - outputvalue))
	else:
		return redirect(url_for('home'))
