docker run -e "MULTILABEL_CLASSIFIER_ENDPOINT=http://govnews-classifier-serve:8000/classifier" --name govnews-classifier-demo --network demo -p 5001:5000 -it govnews-classifier-demo
