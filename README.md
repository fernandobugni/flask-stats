# flask-stats

Flask-stats is a simple plugin that allows you to have important information and statistics for the endpoints that you have. It collects all the data and then you can access it through endpoints live. This plug-in allows to monitor simple api without the necessity of any payment, such as new relic

Status: **working progress**

## Instalation

```cmd
pip install flask-stats
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

In any time, we can enter in ```/endpoint``` to see duration of each endpoint
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

