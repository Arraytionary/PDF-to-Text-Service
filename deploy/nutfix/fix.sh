#!/bin/bash

kubectl delete svc/web
kubectl create -f svc-web.yml
kubectl delete svc/queue-wrapper
kubectl create -f svc-queue-wrapper.yml
kubectl delete svc/minio
kubectl create -f svc-minio.yml
