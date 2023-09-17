# AIAP assessment
* Name: Goh Yun Si
* Email: gohgys97@gmail.com

# Folder structure

```
   .
   └── .github                      
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

## 1. Set-up


## 2. Preprocessing


## 3. Model training


## 4. Model evaluation



# Considerations

## Key findings from EDA


## Features preprocessing
* Pre-trip data and post-trip data are joined by `index` and `Ext_Intcode`.
* Duplicates are removed by keeping the latest (sort `Logging`) passenger submission (keep last `Ext_Intcode`)
* Individual features are processed as summarized in the table below:

| Attribute                                      | Preprocessing                                                                                                                                                                                                                                                                                        |
|------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Gender                                         | * One-hot encoding                                                                                                                                                                                                                                                                                   |
| Date of Birth                                  | * Converted to Age<br>* Unreasonable ages are deleted <br>* Ages are log-transformed to reduce bimodality<br>* Missing data filled with median                                                                                                                                                       |
| Source of Traffic                              | * Split into 2 information: Source Type (Direct / Indirect) and Source Traffic (company website / social media / search engine / email marketing)<br>* One-hot encoding<br>* Missing data filled with median after grouping by possibly related variables(Online Check-in, Cruise Name, Ticket Type) |
| Onboard Wifi Service                           | * Converted to numbers using importance scale<br>* Missing data filled with median after grouping by possibly related variables (Ease of Online booking, Gate location, Embarkation/Disembarkation time convenient)                                                                                  |
| Embarkation/Disembark<br>ation time convenient | * Assume 0 (not in importance scale) to be missing data<br>* Missing data filled with median after grouping by possibly related variables (Ease of Online Booking, Onboard Wifi Service, Gate location)                                                                                              |
| Ease of Online booking                         | * Assume 0 (not in importance scale) to be missing data<br>* Missing data filled with median after grouping by possibly related variables (Onboard Wifi Service, Gate location, Embarkation/Disembarkation time convenient)                                                                          |
| Gate location                                  | * Assume 0 (not in importance scale) to be missing data<br>* Missing data filled with median after grouping by possibly related variables (Ease of Online Booking, Onboard Wifi Service, Embarkation/Disembarkation time convenient)                                                                 |
| Logging                                        | * Dropped assuming time of survey submission is not helpful to prediction                                                                                                                                                                                                                            |
| Onboard Dining Service                         | * Converted to numbers using importance scale<br>* Missing data filled with median after grouping by possibly related variables (Cabin Comfort, Onboard Entertainment, Cleanliness)                                                                                                                  |
| Online Check-in                                | * Assume 0 (not in importance scale) to be missing data<br>* Missing data filled with median after grouping by possibly related variables(Source Type, Source Traffic, Cruise Name, Ticket Type)                                                                                                     |
| Cabin Comfort                                  | * Assume 0 (not in importance scale) to be missing data<br>* Missing data filled with median after grouping by possibly related variables (Onboard Dining Service, Onboard Entertainment, Cleanliness)                                                                                               |
| Onboard Entertainment                          | * Converted to numbers using importance scale<br>* Missing data filled with median after grouping by possibly related variables (Onboard Dining Service, Cabin Comfort, Cleanliness)                                                                                                                 |
| Cabin Service                                  | * Assume 0 (not in importance scale) to be missing data<br>* Missing data filled with median after grouping by possibly related variables (Baggage Handling, Onboard Service)                                                                                                                        |
| Baggage Handling                               | * Missing data filled with median after grouping by possibly related variables (Cabin Service, Onboard Service)                                                                                                                                                                                      |
| Port Check-in Service                          | * Missing data filled with simple median imputation                                                                                                                                                                                                                                                  |
| Onboard Service                                | * Assume 0 (not in importance scale) to be missing data<br>* Missing data filled with median after grouping by possibly related variables (Cabin Service, Baggage Handling)                                                                                                                          |
| Cleanliness                                    | * Assume 0 (not in importance scale) to be missing data<br>* Missing data filled with median after grouping by possibly related variables (Onboard Dining Service, Cabin Comfort, Onboard Entertainment)                                                                                             |
| Ext_Intcode                                    | * Dropped as internal code is not helpful to prediction                                                                                                                                                                                                                                              |
| Cruise Name                                    | * Standardize name: Blastoise / Lapras<br>* One-hot encoding<br>* Missing data filled with median after grouping by possibly related variables(Source Type, Source Traffic, Online Check-in, Ticket Type)                                                                                            |
| Ticket Type                                    | * Converted to numbers using price/prestige of tickets<br>* Missing data filled with median after grouping by possibly related variables(Source Type, Source Traffic, Cruise Name, Online Check-in)                                                                                                  |
| Cruise Distance                                | * Standardize unit: km<br>* Convert negative distance to positive (absolute distance)<br>* Distances are log-transformed to reduce skewness<br>* Missing data filled with median                                                                                                                     |
| WiFi                                           | * Assume 0 (not in importance scale) to be missing data<br>* Dropped as a large proportion is missing data                                                                                                                                                                                           |
| Dining                                         | * Assume missing if all other post-trip information are missing<br>* Missing data filled with simple median imputation                                                                                                                                                                               |
| Entertainment                                  | * Assume 0 (not in importance scale) to be missing data<br>* Dropped as a large proportion is missing data                                                                                                                                                                                           |

## Choice of models
1. Random Forest (RF)
    * Explanation
2. Support Vector Machine (SVM)