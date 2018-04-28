import prometheus_client
from flask import Flask, Response
import yaml

app = Flask(__name__)

CONF_YAML = './sh_exporter.yml'
CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')
PORT = 9119
DEBUG = True

Config = None
Gauges = []
Counts = []
Summaries = []


def create_metric(name, metric_type, description, labels):
    if metric_type == 'gauge':
        Gauges.append(prometheus_client.Gauge(name, description, labels))
    # TODO: Support more types as counts, summaries...
    else:
        raise TypeError('Type {metric_type} is not valid'.format(metric_type=metric_type))


def update_metric(name, metric_type, description, cmd, labels):


def read_conf(yml_path):
    with open(CONF_YAML, "r") as file:
        Config = yaml.safe_load(file)

    for metric in Config.get('sh'):
        name = metric.get('name')
        metric_type = metric.get('type')
        description = metric.get('description')
        for label in metric.get('labels'):
            create_metric(name, metric_type, description, label)

        #g = prometheus_client.Gauge('my_requests_total', 'HTTP Failures', ['method', 'endpoint'])
        #g.labels(method='bb', endpoint='aa').set(5.6)


def update_metrics():
    for metric in Config.get('sh'):
        name = metric.get('name')
        metric_type = metric.get('type')
        description = metric.get('description')
        for label in metric.get('labels'):
            cmd = label.get('cmd')
            update_metric(name, metric_type, description, cmd, label)

@app.route('/metrics')
def metrics():
    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)


read_conf(CONF_YAML)

if __name__ == '__main__':
    app.run(port=PORT, debug=DEBUG)
