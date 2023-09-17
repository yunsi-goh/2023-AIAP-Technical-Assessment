#!/bin/bash

# 1. Set-up
echo "1. Set-up"
conda install --yes --file requirements.txt

# 2. Preprocessing
echo "2. Preprocessing"
python src/preprocessing.py --pre ../data/cruise_pre.db --post ../data/cruise_post.db\
