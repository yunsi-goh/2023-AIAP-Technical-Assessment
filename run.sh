#!/bin/bash


# Define arguments
in_dir="../data"
model_type="RF"
model_name="model_RF"


# Parse command-line arguments using the Python script
while getopts "i:t:n" opt; do
    case "$opt" in
        i)
            in_dir="$OPTARG"
            ;;
        t)
            model_type="$OPTARG"
            ;;
        n)
            model_name="$OPTARG"
            ;;
        \?)
            echo "Usage: $0 [-i in_dir] [-t model_type] [-n model_name] "
            exit 1
            ;;
    esac
done


# 1. Preprocessing
echo "1. Preprocessing"
python src/preprocessing.py -i "$in_dir"

# 2. Model training
echo "2. Model training"
python src/train.py -t "$model_type" -n "$model_name"

# 3. Model evaluation
echo "3. Model evaluation"
python src/evaluate.py -n "$model_name"
