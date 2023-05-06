#!/bin/sh

DATASET_DIR=${PWD}/busi_dataset

echo $DATASET_DIR

python3 train.py --dataset ${DATASET_DIR} \
                 --arch UNext \
                 --name busi \
                 --img_ext .png \
                 --mask_ext .png \
                 --lr 0.0001 \
                 --epochs 500 \
                 --input_w 512 \
                 --input_h 512 \
                 --b 8