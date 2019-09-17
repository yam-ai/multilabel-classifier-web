# Multilabel Classifier Web Frontend

## Build the docker image

```sh
docker build -t yamai/multilabel-classifier-web .
```

## Run the docker image

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
docker run -e "MLC_ENDPOINT=http://back:8000/classifier" -e "MLC_HOST_PORT=0.0.0.0:5000" -p 5000:5000 --name front --network mlc-net -it yamai/multilabel-classifier-web
```

## Access the web frontend

Based on the above configuration, open the URL https://localhost:5000 on a browser.
