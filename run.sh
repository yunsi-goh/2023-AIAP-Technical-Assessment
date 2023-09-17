#!/bin/bash


# Define arguments
in_dir="../data"
model_choice="RF"

# Parse command-line arguments using the Python script
while getopts "i:m" opt; do
    case "$opt" in
        i)
            in_dir="$OPTARG"
            ;;
        m)
            model_choice="$OPTARG"
            ;;
        \?)
            echo "Usage: $0 [-i in_dir] [-m model_choice] "
            exit 1
            ;;
    esac
done


# 1. Set-up
echo "1. Set-up"
conda install --yes --file requirements.txt

# 2. Preprocessing
echo "2. Preprocessing"
python src/preprocessing.py -i "$in_dir"

# 3. Model training
echo "3. Model training"
#python src/train.py -m "RF"

# 4. Model evaluation
echo "4. Model evaluation"
