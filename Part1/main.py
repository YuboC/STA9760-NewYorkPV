
import os

import argparse

from src.nycvk.api import get_data

if __name__ == "__main__":

	app_key = os.getenv(f'APP_KEY')

	parser = argparse.ArgumentParser()
	parser.add_argument("--page_size", type=int)
	parser.add_argument("--num_pages", default=None, type=int)
	parser.add_argument("--output", default=None)
	args = parser.parse_args()
    
	data=get_data(app_key, args.page_size, args.num_pages)
	with open(args.output, "w") as file: 	
		for lis in data:
			for dic in lis:
				file.write(f"{dic}"+'\n')

	