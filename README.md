api
-------

## initialisation

The script init.py initialize a mongo database with the clickstream dataset (http://datahub.io/dataset/wikipedia-clickstream/resource/be85cc68-d1e6-4134-804a-fd36b94dbb82). The script need to be personnalize to indicate the location of the dataset and the configuration of the mongo database.

## usage

```
$ source e/py/bin/activate
(py)$ cd api
(py)$ python init.py
```

## installation

### python dependencies

```
$ source e/py/bin/activate
(py)$ cd api
(py)$ pip install -r requirements.txt
```

## usage

```
$ source e/py/bin/activate
(py)$ cd api
(py)$ api.py
```
