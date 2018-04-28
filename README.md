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
    label:
      - none: 'users'
        cmd: 'who | wc -l'

  - name: 'web_instances'
    type: 'gauge'
    description: 'Number of web instances running'
    label:
      - app: 'chrome'
        cmd: 'ps -ef | grep chrome | wc -l'
      - app: 'firefox'
        cmd: 'ps -ef | grep chrome | wc -l'
```

## Run

