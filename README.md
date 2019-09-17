# Multilabel Text Classifier Web Frontend

## Usage

### Build the docker image

```sh
docker build -t yamai/multilabel-classifier-web .
```

### Run the docker image

Create the docker network:

```sh
docker network create mlc-net
```

Run the multilabel text classifier backend:

```sh
docker run -v $MODEL_DIR:/model -p 8000:8000 --name backend --network mlc-net yamai/fasttext-multilabel-classifier:serve-latest
```

Run the multilabel text classifier frontend:

```sh
docker run -e "MLC_ENDPOINT=http://backend:8000/classifier" -e "MLC_HOST_PORT=0.0.0.0:5000" -p 5000:5000 --name frontend --network mlc-net -it yamai/multilabel-classifier-web
```

You may change the default settings by mapping your customized `settings.py` in the host (e.g., under `/home/mlc/`) to `/web/settings.py` in the container as follows:

```sh
docker run -e "MLC_ENDPOINT=http://backend:8000/classifier" -e "MLC_HOST_PORT=0.0.0.0:5000" -p 5000:5000 --name frontend --network mlc-net -v /home/mlc/settings.py:/web/settings.py -it yamai/multilabel-classifier-web
```

### Access the web frontend

With the above configuration, you may open the URL https://localhost:5000 on a browser to access the Multilabel Text Classifier Web Frontend.

## Professional services

If you need any supporting resources or consultancy services from YAM AI Machinery, please find us at:

* https://www.yam.ai
* https://twitter.com/theYAMai
* https://www.linkedin.com/company/yamai
* https://www.facebook.com/theYAMai
* https://github.com/yam-ai
* https://hub.docker.com/u/yamai
