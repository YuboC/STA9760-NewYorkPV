from datetime import datetime, date
from elasticsearch import Elasticsearch
from requests import get

#create an index
def create_and_update_index(index_name):
	es = Elasticsearch()
	try:
		es.indices.create(index=index_name)
	except Exception:
		pass
	return es

#Format data from API
def data_format(data):
	for key,value in data.items():
		if 'amount' in key:
			data[key] = float(value)
		elif 'number' in key:
			data[key] = int(value)
		elif 'date' in key:
			data[key] = datetime.strptime(data[key], '%m/%d/%Y').date()

#push 
def push_data(data,es,index):
	data_format(data)
	data = es.index(index=index,body=data,id = data['summons_number'])


