
import os

import argparse

from src.bigdata1.api import get_data

if __name__ == "__main__":

	app_key = os.getenv(f'APP_KEY')

	parser = argparse.ArgumentParser()
	parser.add_argument("--page_size", type=int)
	parser.add_argument("--num_pages", default=None, type=int)
	parser.add_argument("--output", default=None)
	parser.add_argument("--push_elastic", default=False, type=bool)
	args = parser.parse_args()
    
	data=get_data(app_key, args.page_size, args.num_pages,args.push_elastic)
	with open(args.output, "w") as file: 	
		for lis in data:
			for dic in lis:
				file.write(f"{dic}"+'\n')
