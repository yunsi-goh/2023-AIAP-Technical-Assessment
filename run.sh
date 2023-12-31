#!/bin/bash


# Set model
model_type="KNN"  # RF: Random Forest | SVM: Support Vector Machine | KNN: K-Nearest Neighbour
model_name="model_KNN"  # Name of model to export


# Parse command-line arguments using the Python script
while getopts "t:n" opt; do
    case "$opt" in
        t)
            model_type="$OPTARG"
            ;;
        n)
            model_name="$OPTARG"
            ;;
        \?)
            echo "Usage: $0 [-t model_type] [-n model_name] "
            exit 1
            ;;
    esac
done


# 1. Preprocessing
echo "1. Preprocessing"
python src/preprocessing.py

# 2. Model training
echo "2. Model training"
python src/train.py -t "$model_type" -n "$model_name"

# 3. Model evaluation
echo "3. Model evaluation"
python src/evaluate.py -n "$model_name"
