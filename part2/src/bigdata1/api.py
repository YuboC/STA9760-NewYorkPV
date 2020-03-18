from sodapy import Socrata
from src.bigdata1.elasticresearch import create_and_update_index, push_data

#Store the data id and domain corresponding to NYC parking violation API
domain = "data.cityofnewyork.us"
dataset_id = 'nc67-uf89'

def get_data(app_key,page_size,num_pages, push_elastic):
	results = []
	client = Socrata(domain,app_key)

	#count the total number of the rows in the API
	rows = int(client.get(dataset_id, select='COUNT(*)')[0]['COUNT'])

	if not num_pages:
		num_pages = rows // page_size + 1

	if push_elastic:
		es = create_and_update_index('bigdata1')
	
	for x in range(0, num_pages):
		results.append(client.get(dataset_id, limit=page_size, offset=x*(page_size)))
		
		if push_elastic:
			push_data(x,es,'bigdata1')
	return results
