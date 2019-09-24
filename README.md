# Multilabel Text Classifier Web Frontend

This is a web frontend for users to query a multilabel text classifier to classify texts they input. The classifier backend engine can be either the [BERT-based multi-label text classification engine](https://github.com/yam-ai/bert-multilabel-classifier) or [fastText-based multi-label text classification engine](https://github.com/yam-ai/fasttext-multilabel-classifier). 

## Usage

You can either [build the docker image from the source code](#build-the-docker-image) or [pull the docker images directly from the Docker Hub](#pull-the-docker-image-from-docker-hub)

### Build the docker image

You can build the docker image from the source code by running the following command in the project directory as follows:

```sh
docker build -t yamai/multilabel-classifier-web .
```

### Pull the docker image from Docker Hub

Without building the docker image from the source code, you can pull the docker image from the [Docker Hub](https://hub.docker.com/r/yamai/multilabel-classifier-web) as follows:

```sh
docker pull yamai/multilabel-classifier-web:latest
```

### Run the docker images

You need to create a docker network (e.g., `mlc-net`) for connecting this Multilabel Text Classifier Web Frontend and the text classifier backend engine as follows:

```sh
docker network create mlc-net
```

Run the text classifier backend engine, e.g., [fast-text-multilabel-classifier](https://github.com/yam-ai/fasttext-multilabel-classifier), on the created docker network:

```sh
docker run -v $MODEL_DIR:/model -p 8000:8000 --name backend --network mlc-net yamai/fasttext-multilabel-classifier:serve-latest
```

Run the Multilabel Text Classifier Web Frontend, on the created docker network:

```sh
docker run -e "MLC_ENDPOINT=http://backend:8000/classifier" -e "MLC_HOST_PORT=0.0.0.0:5000" -p 5000:5000 --name frontend --network mlc-net -it yamai/multilabel-classifier-web
```

### Change the settings if necessary

You may change the default settings by mapping your customized [`settings.py`](https://github.com/yam-ai/multilabel-classifier-web/blob/master/settings.py) in the host (e.g., under `/home/mlc/`) to `/web/settings.py` in the container as follows:

```sh
docker run -e "MLC_ENDPOINT=http://backend:8000/classifier" -e "MLC_HOST_PORT=0.0.0.0:5000" -p 5000:5000 --name frontend --network mlc-net -v /home/mlc/settings.py:/web/settings.py -it yamai/multilabel-classifier-web
```

These settings are as follows:

* `THRESHOLD`: the label of which the likelihood is above this threshold will be shown in bold, e.g., `0.5`.
* `ENDPOINT`: the default endpoint of the multilabel text classifier backend, e.g., `http://0.0.0.0:8000/classifier`.
* `HOST_PORT`: the default host and port for serving this web frontend, e.g., `0.0.0.0:5000`.
* `TITLE`: the title shown on this web frontend.

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
