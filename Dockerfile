FROM python:3

## Install usefull commands
RUN apt-get update && \
    apt --fix-broken install -y && \
	  apt-get install -y jq

# Clean apt
RUN apt-get clean && \
	  rm -rf /var/lib/apt/lists/* && \
	  rm -rf /var/cache/jq

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "./sh_exporter.py" ]