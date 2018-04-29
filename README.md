# Prometheus SH Exporter

Run your own console commands defined in a yaml file and export the outputs in
prometheus metrics format.

## Setup

In order to run you only have to install the requirements defined in requirements.txt

```bash
pip install -r requirements.txt

```

## Yaml File Example

This is a example file of the yaml that defines, the prometheus type, the commands to be run and each tags

```yaml
sh:
  - name: 'users'
    type: 'gauge'
    description: 'Number of users logged in the system'
    cmd: 'who | wc -l'

  - name: 'web_instances_chrome'
    type: 'gauge'
    description: 'Number of chrome instances running'
    cmd: 'ps -ef | grep chrome | wc -l'

  - name: 'process_running'
    type: 'gauge'
    description: 'Number of process running'
    cmd: 'ps -ef | wc -l'
```

## Run

```bash
python sh_exporter.py

```
