# AIAP assessment
* Name: Goh Yun Si
* Email: gohgys97@gmail.com

# Folder structure

```
   .
   └── .github     
   └── data                         <--- [not uploaded] input data folder
   └── output                       <--- output folder             
   └── src                          
   │    ├── config.py               <--- script for setting training parameters
   │    ├── evaluate.py             <--- script to evaluate models
   │    ├── load.py                 <--- script to load preprocessed data
   │    ├── metrics.py              <--- script containing evaluation metric functions
   │    ├── models.py               <--- script containing different models
   │    ├── preprocessing.py        <--- script for data preprocessing
   │    └── train.py                <--- script to train models
   └── .gitattributes
   └── .gitignore
   └── Readme.md                    <--- repository description
   └── eda.ipynb                    <--- exploratory data analysis
   └── requirements.txt             <--- dependencies
   └── run.sh                       <--- executable bash script
``` 

# Code flow

## 0. Setup
   1. In __run.sh__, set the model to use:
      * Line 5: *model_type*
        * RF: Random Forest
        * SVM: Support Vector Machine
        * KNN: K-Nearest Neighbour
      * Line 6: *model_name*
   2. Execute the __run.sh__ file to run the commands in steps 1 - 3.

## 1. Preprocessing
Command executed by __run.sh__:
```
python src/preprocessing.py
```
This script preprocess the cruise data in the following order:
1. Load and merge pre-trip and post-trip data.
2. Rename columns to keep them succinct.
3. Remove duplicate submissions by each passenger.
4. Clean up each feature and perform feature engineering.
5. Transform features if necessary.
6. Impute missing data.
7. Export preprocessed data to: "output/preprocessed.csv"

## 2. Model training
Command executed by __run.sh__:
```
python src/train.py -t "$model_type" -n "$model_name"
``` 
The procedure for model training is as follows:
1. "load.py" is used to import and split the preprocessed data into train and test set.
   * The split ratio can be changed by setting *test_size* in "config.py"
2. "models.py" is used to build and train the various models available.
   * Training configurations can be changed by setting *RF_params*, *SVM_params*, or *KNN_params* in "config.py"
3. Final model is exported to: "output/{model_name}.pkl"

## 3. Model evaluation
Command executed by __run.sh__:
```
python src/evaluate.py -n "$model_name"
``` 
The procedure for model evaluation is as follows:
1. "load.py" is used to import and split the preprocessed data into train and test set.
   * The train and test set will be consistent with the dataset used for model training as long as *test_size*
     and *random_state* in "config.py" remains unchanged.
2. "metrics.py" is used to evaluate model fit on both train and test set using the following metrics
   * Confusion matrix
   * Normalized confusion matrix
   * Mean accuracy

# Considerations

## Key findings from EDA


## Features preprocessing
* Pre-trip data and post-trip data are joined by `index` and `Ext_Intcode`.
* Duplicates are removed by keeping the latest (sort `Logging`) passenger submission (keep last `Ext_Intcode`)
* Individual features are processed as summarized in the table below:

| Attribute                                   | Cleaning & Feature Engineering                                                                                                                                          | Transformation                                     | Imputation                                                                     |
|---------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|--------------------------------------------------------------------------------|
| Gender                                      | * One-hot encoding                                                                                                                                                      | -                                                  | * None column dropped after one-hot encoding                                   |
| Date of Birth                               | * Converted to Age<br>* Unreasonable ages are deleted                                                                                                                   | * Ages are log-transformed to reduce bimodality    | * Missing data filled with simple median imputation                            |
| Source of Traffic                           | * Split into 2 information: Source Type (Direct / Indirect) and Source Traffic (company website / social media / search engine / email marketing)<br>* One-hot encoding | -                                                  | * None column dropped after one-hot encoding                                   |
| Onboard Wifi Service                        | * Converted to numbers using importance scale                                                                                                                           | -                                                  | * Missing data filled with median after grouping by possibly related variables |
| Embarkation/Disembarkation time convenient  | * Assume 0 (not in importance scale) to be missing data                                                                                                                 | -                                                  | * Missing data filled with median after grouping by possibly related variables |
| Ease of Online booking                      | * Assume 0 (not in importance scale) to be missing data                                                                                                                 | -                                                  | * Missing data filled with median after grouping by possibly related variables |
| Gate location                               | * Assume 0 (not in importance scale) to be missing data                                                                                                                 | -                                                  | * Missing data filled with median after grouping by possibly related variables |
| Logging                                     | * Dropped assuming time of survey submission is not helpful to prediction                                                                                               | -                                                  | -                                                                              |
| Onboard Dining Service                      | * Converted to numbers using importance scale                                                                                                                           | -                                                  | * Missing data filled with median after grouping by possibly related variables |
| Online Check-in                             | * Assume 0 (not in importance scale) to be missing data                                                                                                                 | -                                                  | * Missing data filled with median after grouping by possibly related variables |
| Cabin Comfort                               | * Assume 0 (not in importance scale) to be missing data                                                                                                                 | -                                                  | * Missing data filled with median after grouping by possibly related variables |
| Onboard Entertainment                       | * Converted to numbers using importance scale                                                                                                                           | -                                                  | * Missing data filled with median after grouping by possibly related variables |
| Cabin Service                               | * Assume 0 (not in importance scale) to be missing data                                                                                                                 | -                                                  | * Missing data filled with median after grouping by possibly related variables |
| Baggage Handling                            | -                                                                                                                                                                       | -                                                  | * Missing data filled with median after grouping by possibly related variables |
| Port Check-in Service                       | -                                                                                                                                                                       | -                                                  | * Missing data filled with simple median imputation                            |
| Onboard Service                             | * Assume 0 (not in importance scale) to be missing data                                                                                                                 | -                                                  | * Missing data filled with median after grouping by possibly related variables |
| Cleanliness                                 | * Assume 0 (not in importance scale) to be missing data                                                                                                                 | -                                                  | * Missing data filled with median after grouping by possibly related variables |
| Ext_Intcode                                 | * Dropped as internal code is not helpful to prediction                                                                                                                 | -                                                  | -                                                                              |
| Cruise Name                                 | * Standardize name: Blastoise / Lapras<br>* One-hot encoding                                                                                                            | -                                                  | * None column dropped after one-hot encoding                                   |
| Ticket Type                                 | * Converted to numbers using price/prestige of tickets                                                                                                                  | -                                                  | * Missing data filled with median after grouping by possibly related variables |
| Cruise Distance                             | * Standardize unit: km<br>* Convert negative distance to positive (absolute distance)                                                                                   | * Distances are log-transformed to reduce skewness | * Missing data filled with simple median imputation                            |
| WiFi                                        | * Assume 0 (not in importance scale) to be missing data                                                                                                                 | -                                                  | * Dropped as a large proportion is missing data                                |
| Dining                                      | * Assume missing if all other post-trip information are missing                                                                                                         | -                                                  | * Missing data filled with simple median imputation                            |
| Entertainment                               | * Assume 0 (not in importance scale) to be missing data                                                                                                                 | -                                                  | * Dropped as a large proportion is missing data                                |


## Choice of models
1. Random Forest (RF)
   * 
2. Support Vector Machine (SVM)
   *
3. K-Nearest Neighbour (KNN)
   *

## Choice of evaluation metrics
   * Confusion matrix
   * Normalized confusion matrix
   * Mean accuracy

## Conclusion
