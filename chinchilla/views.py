from flask import render_template, jsonify, redirect, url_for, request
from time import strftime, localtime
from chinchilla import app, blocksDB, txDB

@app.route('/')
def home():
	try:
		if request.args.get('page'):
			page = int(request.args.get('page')) - 1
		else:
			page = 0

		blockCount = blocksDB.count()
		blockArray = []

		maxPage = int((blockCount - 19)/20)
		delta = blockCount - page*20

		print(delta)

		pages = {'current' : page, 'max' : maxPage}

		for i in range(delta - 19, delta + 1):
			if i > 0:
				block = blocksDB.find_one({ 'height' : i })
				block['time'] = strftime("%d %b %Y %H:%M:%S", localtime(block['time']))
				blockArray.append(block)

		return render_template('home.html', blocks=blockArray[::-1], pages=pages)
		
		except:
			return render_template('error.html')
		
@app.route('/block/<string:hash>')
def block(hash):
	try:
		blockInfo = blocksDB.find_one({ 'hash' : hash })
		height = blockInfo['height']

		txArray = []

		for i in blockInfo['tx']:
			tx = txDB.find_one({ 'hash' : i })

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
			if j['scriptPubKey']['type'] == 'pubkeyhash':
				addresses = j['scriptPubKey']['addresses']
				value = float(j['value'])
				outputvalue += value
				vout.append({'value' : '{0:.8f}'.format(value), 'addresses' : addresses})

		if len(tx['vin']) == 1 and not 'vout' in tx['vin'][0]:
			vin.append({'value' : 'Generación de Chauchas', 'addresses' : ['Generación de Chauchas']})

		else:
			for i in tx['vin']:
				tx = txDB.find_one({ 'txid' : i['txid'] })
				n = i['vout']

				addresses = tx['vout'][n]['scriptPubKey']['addresses']
				value = float(tx['vout'][n]['value'])
				inputvalue += value
				vin.append({'value' : '{0:.8f}'.format(value), 'addresses' : addresses})

		return render_template('tx.html', vout=vout, vin=vin, txid=txid, fee=inputvalue - outputvalue)
	except:
		return render_template('error.html')