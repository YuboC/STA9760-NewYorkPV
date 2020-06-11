# New York City Parking Violations
[![GitHub stars](https://img.shields.io/github/stars/YuboC/STA9760-NewYorkPV.svg?style=flat&label=Star)](https://github.com/YuboC/STA9760-NewYorkPV/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/YuboC/STA9760-NewYorkPV.svg?style=flat&label=Fork)](https://github.com/YuboC/STA9760-NewYorkPV/fork)
[![GitHub watchers](https://img.shields.io/github/watchers/YuboC/STA9760-NewYorkPV.svg?style=flat&label=Watch)](https://github.com/YuboC/STA9760-NewYorkPV/watchers)

![](https://github.com/YuboC/STA9760-NewYorkPV/blob/master/Part3_visualization/Visualization.PNG)

![](https://media.giphy.com/media/44VMzCwVi6iEU/giphy.gif)

```
This project will load and then analyze a dataset containing millions of NYC 
parking violations since January 2016. By completing this project, 
demonstrating mastery of principles of containerization, terminal navigation, 
python scripting, artifact deployment and AWS EC2 provisioning will be inclued.
```

*readme format credit to [jng985](https://github.com/jng985/parking_violations)

## Part 1: Python Scripting


### Download the files and Use [Docker](https://www.docker.com/) to build the image and run the python file in it.

```bash
docker build -t nycvk:1.0 .
```
### Or pull it from [Dockerhub](https://hub.docker.com/repository/docker/lalagola/nyvio/) in Terminal：
```bash
docker pull lalagola/nyvio:2.0
```
`
- Command line for `Windows` User in `PowerShell`:
```console
docker run -v "$(pwd):/app" -e APP_KEY=YOUR_APP_KEY -t lalagola/nyvio:1.0 python main.py --page_size=1000 --num_pages=4 --output=results2.json
```
- Command line for `Mac` User in `Terminal`:
```console
docker run -v $(pwd):/app -e APP_KEY=YOUR_APP_KEY -t lalagola/nyvio:1.0 python main.py --page_size=1000 --num_pages=4 --output=results2.json
```
### File Structure
  ```console
  .
  ├── Dockerfile
  ├── README.md
  ├── main.py
  ├── requirements.txt
  └── src
      └── nycvk
          └── api.py

  2 directories, 4 files
  ```

#### Arguments

- `--page_size`: 

  - **Required**
  - How many records to request from the API per call.
  
- `--num_pages`: 

  - *Optional*
  - If not provided, continue requesting data until the entirety of the content has been exhausted. 
  - If provided, continue querying for data `num_pages` times.
  
- `--output`: 

  - *Optional*
  - If not provided, print results to stdout. 
  - If provided, write the data to the file `output`.
  
### Example of the output:
- Keys: `plate` `state` `license_type` `summons_number` `issue_date` `summons_image` `description`
```json
{'plate': '2602DLM', 'state': 'NJ', 'license_type': 'PAS', 'summons_number': '8349024859', 'issue_date': '09/24/2016', 'summons_image': {'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSTk1FOVVRWGxPUkdjeFQxRTlQUT09&locationName=_____________________', 'description': 'View Summons'}}
{'plate': '28565MH', 'state': 'NY', 'license_type': 'CSP', 'summons_number': '8349025189', 'issue_date': '09/28/2016', 'summons_image': {'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSTk1FOVVRWGxPVkVVMFQxRTlQUT09&locationName=_____________________', 'description': 'View Summons'}}

```
  
### Deploy to Dockerhub

- Build docker image if necessary
  ```console
  $ docker build -t nycvk:1.0 .
  ```

- Get the `UUID` of the desired image
  ```console
  $ docker images | grep nycvk
  ```

- Tag the image with dockerhub username **with** the version number
  ```console
  $ docker tag {*Insert UUID*} lalagola/nycvk:1.0
  ```

- Push docker image **without** the [TAG]
  ```console
  $ docker push lalagola/nycvk
  ```

#### ssh into AWS EC2 ubuntu instance

- Change directory to the folder containing `.pem` file

- Change `.pem` file permissions to **read-only**

- call commands in Terminal:
  ```console
  $ chmod 0400 {*Insert .pem File*}
  ```

- ssh into the EC2 instance
  ```console
  $ ssh -i {*Insert .pem File*} ubuntu@{*Insert Public IP*}
  ```
#### Docker setup 

Note: When using docker **within** the EC2 instance, the `sudo` command **must** be run. It is possible to make it so that it isn't required, but this is the case "out of the box".

- Update and install `docker.io`
  ```console
  $ sudo apt-get update
  $ sudo apt install docker.io
  ```

- Log in docker
  ```console
  $ sudo docker login --username=lalagola
  ```
  
- Export environment variable `APP_KEY`
  ```console
  $ export APP_KEY={*Insert App Token*}
  ```

#### Run docker modules
```console
 tanaydocker/bigdata1
sudo docker run -v $(PWD):/app/out -e APP_TOKEN=${APP_TOKEN}  -it lalagola/nyvio:3.0 python -m main --page_size=2 --num_pages=5 --output=./out/results.json
```

- `sudo docker run`

  - `-e APP_KEY=${APP_KEY}`
  
  - `-v ${PWD}:/app/out`
  
    - This loads the current working directory into the `out` directory within the docker container
    
  - `-it lalagola/nyvio:3.0`
  
  - `python -m main` 
  
    - `--page_size={*Insert Page Size*}` 
    
    - `--num_pages={*Insert Num Pages*}`
    
    - `--output=./out/{*Insert Output Filename*}`
  
  - if `page_size` and `num_pages` are given, `page_size` * `num_pages` should be printed to stdout
  
  
## Part 2: Loading into ElasticSearch	
```
In this second part, we want to leverage docker-compose to bring up a service that encapsulates 
our bigdata1 container and an  elasticsearch container and ensures that they are able to interact. 
```
### Download from Github

### Command Line:
```console
$ docker-compose run -e APP_KEY=$soda_token -v $(PWD):/app pyth python -m main --page_size=100 --num_pages=1000 --output=./out/results.json
```
- `-e APP_KEY=`: value behind it been created as environment variable
- `-v $(pwd):/app`: mount the current folder to container to sync any changes from local file to file in container
- `pyth python -m main`: run main.py in python image

### WorkFlow after command above：
- 1.  run `main.py`:
  ```python
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
  ```
- 2. run function: `get_data(app_key, args.page_size, args.num_pages, args.push_elastic)` from `api.py`
- 3. run `part2/src/bigdata1/api.py`
  ```python
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
		data_cache = client.get(dataset_id, limit=page_size, offset=x*(page_size))
		results.append(data_cache)
		for data in data_cache:
			if push_elastic:
				push_data(data,es,'bigdata1')
	return results
  ```
 - 4. run `part2/src/bigdata1/elasticsearch.py`
 ```python
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
   ``` 

## Part 3: Visualizing and Analysis on Kibana	
### Visit `localhost:9200` to check Elasticsearch avaliable with the following feedback:
```
{
  "name" : "ApGsh9y",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "_kOj-Nj3QtezpYoadBusuQ",
  "version" : {
    "number" : "6.3.2",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "053779d",
    "build_date" : "2018-07-20T05:20:23.451332Z",
    "build_snapshot" : false,
    "lucene_version" : "7.3.1",
    "minimum_wire_compatibility_version" : "5.6.0",
    "minimum_index_compatibility_version" : "5.0.0"
  },
  "tagline" : "You Know, for Search"
}
```
### Visit `localhost:5601` to connect Kibana

- Turn on query features
![](https://github.com/YuboC/STA9760-NewYorkPV/blob/master/Part3_visualization/Turn_on_query_features.PNG)

- Configure settings
![](https://github.com/YuboC/STA9760-NewYorkPV/blob/master/Part3_visualization/configure_settings.png)

- Add Visualizations to Dashboard
![](https://github.com/YuboC/STA9760-NewYorkPV/blob/master/Part3_visualization/Visualization.PNG)
 - Time-series chart:
 ```consel
 .es(index=nyc, timefield=Date, metric=count).points(fill=5).color(pink).label(‘Count’).yaxis(label=“Count”), 
 .es(index=nyc, timefield=Date,metric=count).movingaverage(12).lines().color(aqua).label(‘Movingaverage’)
 ```

## Part 4: Deploying to EC2 Instance	




