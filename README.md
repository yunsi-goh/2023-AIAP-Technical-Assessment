# AIAP assessment
* Name: Goh Yun Si
* Email: gohgys97@gmail.com

# Folder structure
```
   .
   ├── .github     
   ├── data                         <--- input data folder [NOT UPLOADED - as per instruction]
   │    ├── cruise_pre.db
   │    └── cruise_post.db
   ├── output
   │    ├── evaluate_KNN.log        <--- log for model evaluation [renamed for KNN]
   │    ├── evaluate_RF.log         <--- log for model evaluation [renamed for RF]
   │    ├── evaluate_SVM.log        <--- log for model evaluation [NOT UPLOADED - unable to finish training]
   │    ├── model_KNN.pkl           <--- exported KNN model             
   │    ├── model_RF.pkl            <--- exported RF model [NOT UPLOADED - size too large]  
   │    ├── model_SVM.pkl           <--- exported SVM model [NOT UPLOADED - unable to finish training]
   │    ├── preprocessed.csv        <--- preprocessed data
   │    ├── preprocessing.log       <--- log for preprocessing
   │    ├── train_KNN.log           <--- log for training [renamed for KNN]
   │    ├── train_RF.log            <--- log for training [renamed for RF]
   │    └── train_SVM.log           <--- log for training [NOT UPLOADED - unable to finish training]
   ├── src                          
   │    ├── config.py               <--- script for setting training parameters
   │    ├── evaluate.py             <--- script to evaluate models
   │    ├── load.py                 <--- script to load preprocessed data
   │    ├── metrics.py              <--- script containing evaluation metric functions
   │    ├── models.py               <--- script containing different models
   │    ├── preprocessing.py        <--- script for data preprocessing
   │    └── train.py                <--- script to train models
   ├── .gitattributes
   ├── .gitignore
   ├── Readme.md                    <--- repository description
   ├── eda.ipynb                    <--- exploratory data analysis
   ├── requirements.txt             <--- dependencies
   └── run.sh                       <--- executable bash script
``` 

* NOTE: Due to time constraints, SVM model was not able to finish training.

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
8. Log will be exported to: "output/preprocessing.log"

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
4. Log will be exported to: "output/train.log"

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
3. Log will be exported to: "output/evaluate.log"

# Considerations

## Key findings from EDA

* Individual features:

| Attribute                                      | Key findings                                                                                                                 |
|------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| Gender                                         | * Object type<br>* Nominal categorical data                                                                                  |
| Date of Birth                                  | * Object type (format not standardized)<br>* Can be converted to datetime type<br>* Can be converted to numerical data (age) |
| Source of Traffic                              | * Object type<br>* Nominal categorical data                                                                                  |
| Onboard Wifi Service                           | * Object type<br>* Can be converted to float type and ordinal categorical data using importance scale                        |
| Embarkation/Disembark<br>ation time convenient | * Float type<br>* Ordinal categorical data based on importance scale                                                         |
| Ease of Online booking                         | * Float type<br>* Ordinal categorical data based on importance scale                                                         |
| Gate location                                  | * Float type<br>* Ordinal categorical data based on importance scale                                                         |
| Logging                                        | * Object type<br>* Can be converted to datetime type<br>* May not be useful for prediction                                   |
| Onboard Dining Service                         | * Object type<br>* Can be converted to float type and ordinal categorical data using importance scale                        |
| Online Check-in                                | * Float type<br>* Ordinal categorical data based on importance scale                                                         |
| Cabin Comfort                                  | * Float type<br>* Ordinal categorical data based on importance scale                                                         |
| Onboard Entertainment                          | * Object type<br>* Can be converted to float type and ordinal categorical data using importance scale                        |
| Cabin Service                                  | * Float type<br>* Ordinal categorical data based on importance scale                                                         |
| Baggage Handling                               | * Float type<br>* Ordinal categorical data based on importance scale                                                         |
| Port Check-in Service                          | * Float type<br>* Ordinal categorical data based on importance scale                                                         |
| Onboard Service                                | * Float type<br>* Ordinal categorical data based on importance scale                                                         |
| Cleanliness                                    | * Float type<br>* Ordinal categorical data based on importance scale                                                         |
| Ext_Intcode                                    | * Object type<br>* May not be useful for prediction                                                                          |
| Cruise Name                                    | * Object type (name not standardized) <br>* Nominal categorical data                                                         |
| Ticket Type                                    | * Object type<br>* Can be converted to ordinal categorical data based on ticket price/prestige                               |
| Cruise Distance                                | * Object type (unit not standardized)<br>* Can be converted to numerical data (distance in km)                               |
| WiFi                                           | * Float type<br>* Binary categorical data<br>* Large proportion of data missing                                              |
| Dining                                         | * Int type<br>* Binary categorical data<br>* Unusual that there is no NaN                                                    |
| Entertainment                                  | * Float type<br>* Binary categorical data<br>* Large proportion of data missing                                              |    

* Univariate analysis
  * Age of passenger has a bimodal distribution.
  * Distance of cruise is right-skewed and consists of outliers (although it is possible for a cruise to travel very 
    long distances if it refuels).
  * Passengers seem to value these variable more: 
    * Embarkation/Disembarkation time convenience
    * Onboard Dining Service
    * Online Check-in
    * Cabin Comfort
    * Onboard Entertainment
    * Cabin Service
    * Baggage Handling
    * Port Check-in Service
    * Onboard Service
    * Cleanliness
  * Passengers seem to value these variable less:
    * Onboard Wifi Service
    * Ease of Online Booking
    * Gate location
  * Most passengers purchased Standard and Luxury tickets. Deluxe tickets are much less in-demand.
  * There are mixed feelings (around half-half) on satisfcation level of WiFi, Dining, and Entertainment.
  * There are about equal number of male and female passengers. 
  * Most passengers heard about or booked the cruise through direct channels (Company Website / Email Marketing) instead of indirect channels (Social Media / Search Engine).
  * Blastoise cruise is more popular than Lapras cruise.

* Bivariate analysis
  * Age of passenger and distance of cruise do not seem to be correlated.
  * Overall, these variables may be correlated:
    * Cruise Name - Onboard Wifi Service 
    * Source of Traffic - Embarkation/Disembarkation time convenient 
    * Cruise Name - Ease of Online booking 
    * Cruise Name - Online Check-in 
    * Source of Traffic - Online Check-in 
    * Cruise Name - Cabin Comfort 
    * Source of Traffic - Cabin Comfort 
    * Cruise Name - Onboard Entertainment
    * Source of Traffic - Onboard Entertainment
    * Cruise Name - Cabin Service  
    * Source of Traffic - Cabin Service
    * Cruise Name - Cleanliness 
    * Source of Traffic - Cleanliness 
    * Cruise Name - Ticket Type  
    * Source of Traffic - Ticket Type  
  * As these are categorical data with few classes, it is hard to determine any trends in their relationships.

* Multivariate analysis
  * Overall, these variable may have some correlations:
    * Ease of Online Booking, Onboard Wifi Service, Gate location, Embarkation/Disembarkation time convenient 
    * Cabin Comfort, Onboard Dining Servic, Onboard Entertainment, Cleanliness 
    * Baggage Handling, Cabin Service, Onboard Service

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
| WiFi                                        | -                                                                                                                                                                       | -                                                  | * Dropped as a large proportion is missing data                                |
| Dining                                      | * Assume missing if all other post-trip information are missing                                                                                                         | -                                                  | * Missing data filled with simple median imputation                            |
| Entertainment                               | -                                                                                                                                                                       | -                                                  | * Dropped as a large proportion is missing data                                |

## Choice of models
1. Random Forest (RF)
   * Accurate, generalizes well, and minimizes overfitting by using an ensemble of decision trees.
   * Due to the ensemble method, it is less affected by outliers (which were not removed during preprocessing).
   * Commonly used in other customer behaviour prediction problems as it works well with various unknown distributions
     and non-linear relationships (since there are only 3 ticket types, it is unclear what are the x-y relationships).
   * Able to handle both the numerical and categorical variables (both can be found in the dataset).
   * Works with multiclass classification (since there are 3 target label ticket types)
   * Provides feature importance information.
   
2. Support Vector Machine (SVM)
   * Accurate even with high dimensions (preprocessed data contains 26 features) as different kernels can be used
     to create complex decision boundary in hyperplane.
   * Less affected by outliers as the margin can be adjusted to ignore some outliers (which were not removed during 
     preprocessing).
   * Works with multiclass classification (since there are 3 target label ticket types)
   * Generalizes well and minimizes overfitting via regularization.
   * Linear kernel can provide feature importance information.
   
3. K-Nearest Neighbour (KNN)
   * Work well with various unknown distributions and non-linear relationships (since there are only 3 ticket types, 
     it is unclear what are the x-y relationships).
   * Less affected by outliers (which were not removed during preprocessing) as nearby neighbours have larger effect.
   * Less affected by imbalanced classes (there are much more Standard and Luxury than Deluxe ticket purchase) 
     as nearby neighbours have larger effect.
   * Fast (since there are 90895 training data with 26 features each) as it does not require training.
   * Works with multiclass classification (since there are 3 target label ticket types)

## Choice of evaluation metrics
1. Confusion matrix 
   * Good visualization for multi-class problems (since there are 3 target label ticket types) as it provides a
     quantitative summary of how well the model performs for each class.
   * Can be normalized within each class to account for class imbalance (there are much more Standard and Luxury 
     than Deluxe ticket purchase).

2. Overall accuracy
   * Common baseline for many classification models since it is a quick and easy-to-interpret metrics
     which calculates the overall percentage of correct classifications across all classes.

3. Classification report
    * Includes precision, recall, f1-score, and support.
      * Precision is important for reducing false positives.
      * Recall is important for reducing false negatives.
      * F1-score balances precision and recall and is used when both false positives and false negatives are important.
      * Support counts the number of data points in each class for imbalanced data considerations.
    * Better metrics for imbalanced data (there are much more Standard and Luxury than Deluxe ticket purchase) as it
    also calculates metrics for individual classes.
      * Macro-averaged metrics: computed for each class and averaged
      * Micro-averaged metrics: computed globally

## Results

NOTE: Due to time constraints, SVM model was not able to finish training.

The table below summarizes the results from model training and evaluation. For more details, refer to logs.

|                                   | Random Forest (RF)                                                                                                                                             | Support Vector Machine (SVM) | K-Nearest Neighbour (KNN)                                                                                                                                      |
|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Training time                     | 56 min 24 s                                                                                                                                                    |                              | 3 min 41 s                                                                                                                                                     |
| Training parameters tested        | n_estimators = [100, 200, 500, 1000]<br>max_depth = [None, 2, 5, 10]<br>max_features = ['sqrt', 'log2']                                                        |                              | n_neighbors = [5, 10, 20, 50]<br>weights = ['uniform', 'distance']<br>metric = ['minkowski', 'euclidean', 'manhattan']                                         |
| Best model obtained from training | n_estimators = 1000<br>max_depth = None<br>max_features = log2<br>accuracy = 0.806                                                                             |                              | n_neighbours = 50<br>weights = 'distance'<br>metric = 'manhattan'<br>accuracy = 0.779                                                                          |
| Training overall scores           | accuracy = 1.0<br>precision_macro = 1.0<br>precision_micro = 1.0<br>recall_macro = 1.0<br>recall_micro = 1.0<br>f1_macro = 1.0<br>f1_micro = 1.0               |                              | accuracy = 1.0<br>precision_macro = 1.0<br>precision_micro = 1.0<br>recall_macro = 1.0<br>recall_micro = 1.0<br>f1_macro = 1.0<br>f1_micro = 1.0               |
| Testing overall scores            | accuracy = 0.803<br>precision_macro = 0.618<br>precision_micro = 0.771<br>recall_macro = 0.573<br>recall_micro = 0.803<br>f1_macro = 0.555<br>f1_micro = 0.777 |                              | accuracy = 0.776<br>precision_macro = 0.518<br>precision_micro = 0.727<br>recall_macro = 0.553<br>recall_micro = 0.776<br>f1_macro = 0.535<br>f1_micro = 0.750 |

* Discussion
  * From the higher training scores and lower testing scores for RF and KNN, both models seem to overfit.
  * Comparing RF and KNN testing scores, RF performed better.
  * From "output/evaluate_RF.log", RF was able to classify Standard and Luxury tickets relatively well.
    However, there were a lot of misclassification (false negatives) for Deluxe tickets. This could be due to
    imbalance classes (there were not enough training points for Deluxe tickets). This is also a problem in KNN.