# Prometheus SH Exporter for Pushgateway

Run your own console commands defined in a yaml file and export the outputs to prometheus pushgateway: https://github.com/prometheus/pushgateway.

## Setup

In order to run you only have to install the requirements defined in requirements.txt

```bash
pip install -r requirements.txt

```

## Yaml File Example

This is a example file of the yaml that defines the server where the pushgateway is.
Also the prometheus type metric, job name, instance, description and the commands to be run

```yaml
server: localhost
port: 9091
wait: 10
sh:
  - name: 'users'
    type: 'gauge'
    job: 'users'
    instance: 'a'
    description: 'Number of users logged in the system'
    cmd: 'who | wc -l'

  - name: 'web_instances_chrome'
    type: 'gauge'
    job: 'users2'
    instance: 'a'
    description: 'Number of chrome instances running'
    cmd: 'ps -ef | grep chrome | wc -l'

  - name: 'process_running'
    type: 'gauge'
    job: 'users2'
    instance: 'b'
    description: 'Number of process running'
    cmd: 'ps -ef | wc -l'

```

## Run

```bash
python sh_exporter.py

```
