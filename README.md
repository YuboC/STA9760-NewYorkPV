# New York City Parking Violations
[![GitHub stars](https://img.shields.io/github/stars/YuboC/STA9760-NewYorkPV.svg?style=flat&label=Star)](https://github.com/YuboC/STA9760-NewYorkPV/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/YuboC/STA9760-NewYorkPV.svg?style=flat&label=Fork)](https://github.com/YuboC/STA9760-NewYorkPV/fork)
[![GitHub watchers](https://img.shields.io/github/watchers/YuboC/STA9760-NewYorkPV.svg?style=flat&label=Watch)](https://github.com/YuboC/STA9760-NewYorkPV/watchers)

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
docker pull lalagola/nyvio:1.0
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

### EC2

#### ssh into EC2

- Change directory to the folder containing `.pem` file

- Change `.pem` file permissions to **read-only**
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

- Log in and pull docker image
  ```console
  $ sudo docker login --username=lalagola
  $ sudo docker pull lalagola/nyvio:1.0
  ```

- Export environment variable `APP_KEY`
  ```console
  $ export APP_KEY={*Insert App Token*}
  ```

#### Run docker modules

- `sudo docker run`

  - `-e APP_KEY=${APP_KEY}`
  
  - `-v ${PWD}:/app/out`
  
    - This loads the current working directory into the `out` directory within the docker container
    
  - `-it lalagola/nyvio:1.0`
  
  - `python -m main` 
  
    - `--page_size={*Insert Page Size*}` 
    
    - `--num_pages={*Insert Num Pages*}`
    
    - `--output=./out/{*Insert Output Filename*}`
  
  - if `page_size` and `num_pages` are given, `page_size` * `num_pages` should be printed to stdout
  
  
  
## Part 2: Loading into ElasticSearch	


## Part 3: Visualizing and Analysis on Kibana	


## Part 4: Deploying to EC2 Instance	
