import requests

headers = {
	'Authorization': 'Token ' + str(data['api_key']),
	'Content-Type': 'application/json'
}

payload = {
	'to': str(receiver_number),
	'body': 'En kreditupplysning har tagits, vänta & få den på posten eller läs den med Mobilt BankID i en säker digital brevlåda https://kivra.com/kreditupplysning/cs',
	'from': 'Kivra',
	'encoding': 'UTF-8',
	'receive_dlr': 0
}

request = requests.post('https://api.beepsend.com/2/send/', data=json.dumps(payload), headers=headers)
print request, request.json()