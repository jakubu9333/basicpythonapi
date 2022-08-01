# AMCEF task
Amcef task is microservice api for posts.

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
docker build -t amceftask .
docker run -p 5000:5000 --name amceftask amceftask 
 ```

In both ways application will open on localhost:5000

## 