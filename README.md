# flask-stats

Flask-stats is a simple plugin that allows you to have important information and statistics for the endpoints that you have. It collects all the data and then you can access it through endpoints live. This plug-in allows to monitor simple api without the necessity of any payment, such as new relic

Status: **working progress**

## Instalation

```cmd
pip install flask-api-stats
```

## A Simple Example

```Python
from flask import Flask
from time import sleep
from flask_stats.flask_stats import Stats

app = Flask(__name__)
Stats(app)

@app.route('/')
def hello():
    sleep(10)
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
```

Adding ```Stats(app)``` allows to register statistics of the API such as response time or configuration. 

In any time, we can enter in ```/endpoints_stats``` to see duration of each endpoint
```
{
    duration: [
        {
            endpoint "/" : {
                avg: 10.009691333770752,
                count: 5,
                max: 10.010810375213623,
                min: 10.007489919662476,
                percentile_25: 10.007489919662476,
                percentile_50: 10.01064133644104,
                percentile_75: 10.010623693466187,
                percentile_90: 10.010810375213623
            }
        },
    ...
    ]
}
```
Other endpoint is ```/stats``` where we can see uptime, gc_stats and other configurations

```
{
gc_stats: {
    gc.get_debug: 0,
    gc.get_stats: {
        collected: 5455,
        collections: 130,
        uncollectable: 0
    ...
    },
    uptime: 1210.0311439037323,
    uptime_readable: {
        days: 0,
        hours: 0,
        minutes: 20,
        seconds: 10.0311439037323
    }
}
```

## Contact
Please if you have any doubt or found any bug report and issue or send an email to fernando.bugni(a)gmail.com

<!---
Comments how to update to pypi
==============================
Tutorial: https://packaging.python.org/tutorials/packaging-projects/

Official: https://pypi.org/manage/projects/
Test: https://test.pypi.org/manage/projects/

** Upload package
* python3 -m pip install --user --upgrade setuptools wheel
* python3 setup.py sdist bdist_wheel
    dist/
        example_pkg_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl
        example_pkg_YOUR_USERNAME_HERE-0.0.1.tar.gz
* python3 -m pip install --user --upgrade twine
* python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    Uploading distributions to https://test.pypi.org/legacy/
    Enter your username: [your username]
    Enter your password:
    Uploading example_pkg_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl
    100%|█████████████████████| 4.65k/4.65k [00:01<00:00, 2.88kB/s]

** Installing your newly uploaded package
* Create a new venv
* python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-pkg-YOUR-USERNAME-HERE

** To Upload package for production 
* python3 -m twine upload dist/*

-->