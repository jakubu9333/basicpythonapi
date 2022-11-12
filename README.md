#  Basic python api
Basic python api is microservice api for posts.

## Installation

Download source code.


### Without docker

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```
Run init.py to create database
```bash
python init.py
```
Run app/aplication.py
```bash
python app/aplication.py
```

### Docker
```bash
docker build -t customname .
docker run -p 5000:5000 --name customname customname 
 ```

In both ways application will open on localhost:5000

## Documentation
Documentation is on localhost:5000/
