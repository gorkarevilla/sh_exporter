import time
import requests
from subprocess import check_output
import yaml

CONF_YAML = './sh_exporter.yml'
Server = 'localhost'
Port = 9091
Wait = 30

Config = None
Gauges = []


def create_metric(name, metric_type, description, job, instance, cmd):
    if metric_type == 'gauge':
        Gauges.append([name, description, job, instance, cmd])
    # TODO: Support more types as counts, summaries...
    else:
        raise TypeError('Type {metric_type} is not valid'.format(metric_type=metric_type))


def read_conf(yml_path):
    # TODO: Support Labels in the yml definition
    with open(CONF_YAML, "r") as file:
        Config = yaml.safe_load(file)

    if Config.get('server'):
        global Server
        Server = Config.get('server')
    if Config.get('port'):
        global Port
        Port = Config.get('port')
    if Config.get('wait'):
        global Wait
        Wait = Config.get('wait')

    for metric in Config.get('sh'):
        name = metric.get('name')
        metric_type = metric.get('type')
        description = metric.get('description')
        job = metric.get('job')
        instance = metric.get('instance')
        cmd = metric.get('cmd')
        create_metric(name, metric_type, description, job, instance, cmd)


def update_metrics():
    for name, description, job, instance, cmd in Gauges:
        cmd_output = check_output(cmd, shell=True)
        try:
            value = int(cmd_output)
        except ValueError:
            raise ValueError('Output of CMD {cmd} is not a integer: {output}'.format(cmd=cmd, output=cmd_output))

        url = 'http://{server}:{port}/metrics/job/{job}/instance/{instance}'.format(server=Server, port=Port, job=job,
                                                                             instance=instance)
        data = '{name} {value}\n'.format(name=name, value=value)

        r = requests.post(url=url, data=data, headers={'Content-Type': 'text/plain'})

        if r.status_code != 202:
            print 'Error. Request {request} returns {code} code.'.format(request=r.url, code=r.status_code)


if __name__ == '__main__':
    read_conf(CONF_YAML)
    while True:
        update_metrics()
        time.sleep(Wait)
