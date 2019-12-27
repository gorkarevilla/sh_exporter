import time
import requests
import logging
import os
import argparse
from subprocess import check_output
import yaml

logger = logging.getLogger("sh_exporter")
# Defaults
CONF_YAML = ['./sh_exporter.yml', './sh_exporter.yaml',
             '/etc/sh_exporter/sh_exporter.yml', '/etc/sh_exporter/sh_exporter.yaml',
             '/etc/sh_exporter.yml', '/etc/sh_exporter.yaml']
server = 'localhost'
port = 9091
wait = 30

gauges = []


def create_metric(name, metric_type, description, job, instance, cmd):
    if metric_type == 'gauge':
        gauges.append([name, description, job, instance, cmd])
    # TODO: Support more types as counts, summaries...
    else:
        raise TypeError('Type {metric_type} is not valid'.format(metric_type=metric_type))


def read_conf(yml_path):
    # TODO: Support Labels in the yml definition
    with open(yml_path, "r") as file:
        config = yaml.safe_load(file)

    if config.get('server'):
        global server
        server = config.get('server')
    if config.get('port'):
        global port
        port = config.get('port')
    if config.get('wait'):
        global wait
        wait = config.get('wait')

    for metric in config.get('sh'):
        name = metric.get('name')
        metric_type = metric.get('type')
        description = metric.get('description')
        job = metric.get('job')
        instance = metric.get('instance')
        cmd = metric.get('cmd')
        create_metric(name, metric_type, description, job, instance, cmd)


def update_metrics():
    for name, description, job, instance, cmd in gauges:
        cmd_output = 0
        try:
            cmd_output = check_output(cmd, shell=True)
        except:
            logger.warning('ERROR: CMD {cmd} can not be executed'.format(cmd=cmd))

        value = 0
        try:
            value = int(cmd_output)
        except:
            logger.warning('ERROR: Output of CMD {cmd} is not a integer: {output}'.format(cmd=cmd, output=cmd_output))

        url = 'http://{server}:{port}/metrics/job/{job}/instance/{instance}'.format(server=server, port=port, job=job,
                                                                                    instance=instance)
        data = '{name} {value}\n'.format(name=name, value=value)
        try:
            r = requests.post(url=url, data=data, headers={'Content-Type': 'text/plain'})

            if r.ok:
                logger.info("Metric delivered succesfully: {url} - {data}".format(url=url, data=data))
            else:
                logger.warning(
                    'ERROR: Request {request} returns {code} code.'.format(request=r.url, code=r.status_code))
        except Exception as e:
            logger.warning(str(e))


if __name__ == '__main__':

    # Load arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', action='store', dest='file',
                        help='Config yaml file')

    args = parser.parse_args()

    if args.file is not None:
        CONF_YAML = [args.file]

    config_file = None
    for file in CONF_YAML:
        if os.path.isfile(file):
            config_file = file
            logger.info("Reading config from file in {file}".format(file=file))
            read_conf(file)
            break
    if config_file is None:
        if args.file is not None:
            logger.error("File not found: {}".format(CONF_YAML[0]))
        else:
            logger.error("Any of the default config files found: {}".format(CONF_YAML))
        exit(1)

    while True:
        update_metrics()
        time.sleep(wait)
