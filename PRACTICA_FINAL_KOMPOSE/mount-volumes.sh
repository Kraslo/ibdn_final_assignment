#!/bin/bash

minikube mount ./data_volume/:/data/data_volume &
minikube mount ./model_volume/:/data/model_volume &
minikube mount ./train_volume/:/data/train_volume &
