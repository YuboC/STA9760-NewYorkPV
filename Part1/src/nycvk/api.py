#import pandas as pd

from sodapy import Socrata

def get_data(app_key,page_size,num_pages):

	client = Socrata("data.cityofnewyork.us",app_key)
	results = []
	for x in range(0, num_pages):
		results.append(client.get('nc67-uf89', limit=page_size, offset=x*(page_size)))
	return results
