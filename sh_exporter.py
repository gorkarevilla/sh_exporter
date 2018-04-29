import prometheus_client
from flask import Flask, Response
from subprocess import check_output
import yaml

app = Flask(__name__)

CONF_YAML = './sh_exporter.yml'
CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')
PORT = 9119
DEBUG = False

Config = None
Gauges = []


def create_metric(name, metric_type, description, cmd):
    if metric_type == 'gauge':
        Gauges.append([prometheus_client.Gauge(name, description), cmd])
    # TODO: Support more types as counts, summaries...
    else:
        raise TypeError('Type {metric_type} is not valid'.format(metric_type=metric_type))


def read_conf(yml_path):
    #TODO: Support Labels in the yml definition
    with open(CONF_YAML, "r") as file:
        Config = yaml.safe_load(file)

    for metric in Config.get('sh'):
        name = metric.get('name')
        metric_type = metric.get('type')
        description = metric.get('description')
        cmd = metric.get('cmd')
        create_metric(name, metric_type, description, cmd)


def update_metrics():
    for gauge, cmd in Gauges:
        cmd_output = check_output(cmd, shell=True)
        try:
            gauge.set(int(cmd_output))
        except ValueError:
            raise ValueError('Output of CMD {cmd} is not a integer: {output}'.format(cmd=cmd, output=cmd_output))

@app.route('/metrics')
def metrics():
    update_metrics()
    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    read_conf(CONF_YAML)
    app.run(port=PORT, debug=DEBUG)
