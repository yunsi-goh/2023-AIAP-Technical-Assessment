import os
import logging
import sqlite3
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder


"""
Functions
"""

def load_cruise_data(in_dir):
    print("Loading data...")
    logging.info("Loading data...")

    # Load pre-trip data
    cruise_pre_con = sqlite3.connect(os.path.join(in_dir, "cruise_pre.db"))
    cruise_pre = pd.read_sql_query("SELECT * FROM cruise_pre", cruise_pre_con)

    # Load post-trip data
    cruise_post_con = sqlite3.connect(os.path.join(in_dir, "cruise_post.db"))
    cruise_post = pd.read_sql_query("SELECT * FROM cruise_post", cruise_post_con)

    # Merge pre-trip and post-trip data
    cruise = cruise_pre.merge(cruise_post, on=["index", "Ext_Intcode"])

    return cruise

def rename_cruise_col(cruise):
    print("Renaming columns...")
    logging.info("Renaming columns...")

    # Rename columns
    map_col = {
        "Gender": "gender",
        "Date of Birth": "birth_date",
        "Source of Traffic": "source",
        "Onboard Wifi Service": "wifi_impt",
        "Embarkation/Disembarkation time convenient": "schedule_impt",
        "Ease of Online booking": "booking_impt",
        "Gate location": "gate_impt",
        "Logging": "log_time",
        "Onboard Dining Service": "dining_impt",
        "Online Check-in": "online_checkin_impt",
        "Cabin Comfort": "comfort_impt",
        "Onboard Entertainment": "entertain_impt",
        "Cabin service": "cabin_svc_impt",
        "Baggage handling": "baggage_impt",
        "Port Check-in Service": "port_checkin_impt",
        "Onboard Service": "onboard_svc_impt",
        "Cleanliness": "clean_impt",
        "Cruise Name": "cruise",
        "Ticket Type": "ticket",
        "Cruise Distance": "distance",
        "WiFi": "wifi_satisfy",
        "Dining": "dining_satisfy",
        "Entertainment": "entertain_satisfy"
    }
    cruise = cruise.rename(columns=map_col)

    return cruise

def remove_cruise_duplicates(cruise):
    print("Removing duplicates...")
    logging.info("Removing duplicates...")

    # Convert logtime to datetime and sort by logtime
    cruise["log_time"] = pd.to_datetime(cruise.loc[:, "log_time"], format="%d/%m/%Y %H:%M")
    cruise = cruise.sort_values(by=["log_time"], ignore_index=True)

    # Clean duplicates (keep final submission)
    cruise = cruise.drop_duplicates(subset="Ext_Intcode", keep="last")
    cruise = cruise.reset_index(drop=True)
    cruise = cruise.drop(["index", "Ext_Intcode", "log_time"], axis="columns")

    return cruise

def cruise_ft_eng(cruise):
    print("Feature engineering...")
    logging.info("Feature engineering...")

    """
    Gender (gender)
    """
    # One-hot encoding
    cruise["gender_enc"] = cruise["gender"].astype('category').cat.codes
    enc = OneHotEncoder()
    enc_data = pd.DataFrame(enc.fit_transform(
        cruise[["gender_enc"]]).toarray())

    # Add encoded columns
    enc_data.columns = ["gender." + str(i) for i in cruise["gender"].unique()]
    cruise = cruise.join(enc_data)
    cruise = cruise.drop(["gender_enc", "gender.None"], axis="columns")

    """
    Date of Birth (birth_date)
    """
    # Set current year and max age allowed
    current_year = 2023
    max_age = 116

    # Calculate age
    cruise["age"] = 0
    for i in cruise.index:
        if str(cruise.loc[i, "birth_date"]) == "None":
            cruise.loc[i, "age"] = np.nan
        elif "/" in str(cruise.loc[i, "birth_date"]):
            age = current_year - int(cruise.loc[i, "birth_date"][-4:])
        elif "-" in str(cruise.loc[i, "birth_date"]):
            age = current_year - int(cruise.loc[i, "birth_date"][:4])
        else:
            print("WARNING: Check birth_date for index {}.".format(i))
            logging.warning("Check birth_date for index {}.".format(i))

        # Update age
        if age > max_age:
            cruise.loc[i, "age"] = np.nan
        else:
            cruise.loc[i, "age"] = age

    # Drop original Date of Birth column
    cruise = cruise.drop(["birth_date"], axis="columns")

    """
    Source of Traffic (source)
    """
    # Split source_type and source_traffic
    cruise["source_type"] = "None"
    for i in cruise.index:

        # source_type
        if "Direct" in str(cruise.loc[i, "source"]):
            cruise.loc[i, "source_type"] = "Direct"
        elif "Indirect" in str(cruise.loc[i, "source"]):
            cruise.loc[i, "source_type"] = "Indirect"
        else:
            print("WARNING: Check index {} for source.".format(i))
            logging.warning("Check index {} for source.".format(i))

        # source_traffic
        if "Company Website" in str(cruise.loc[i, "source"]):
            cruise.loc[i, "source_traffic"] = "CompanyWebsite"
        elif "Social Media" in str(cruise.loc[i, "source"]):
            cruise.loc[i, "source_traffic"] = "SocialMedia"
        elif "Search Engine" in str(cruise.loc[i, "source"]):
            cruise.loc[i, "source_traffic"] = "SearchEngine"
        elif "Email Marketing" in str(cruise.loc[i, "source"]):
            cruise.loc[i, "source_traffic"] = "EmailMarketing"
        else:
            print("WARNING: Check index {} for source.".format(i))
            logging.warning("Check index {} for source.".format(i))

    # One-hot encoding
    cruise["source_type_enc"] = cruise["source_type"].astype('category').cat.codes
    cruise["source_traffic_enc"] = cruise["source_traffic"].astype('category').cat.codes
    enc = OneHotEncoder()
    enc_data = pd.DataFrame(enc.fit_transform(
        cruise[["source_type_enc", "source_traffic_enc"]]).toarray())

    # Add encoded columns
    enc_data.columns = ["source_type." + str(i) for i in cruise["source_type"].unique()] + \
                       ["source_traffic." + str(i) for i in cruise["source_traffic"].unique()]
    cruise = cruise.join(enc_data)
    cruise = cruise.drop(["source", "source_type_enc", "source_traffic_enc"], axis="columns")

    """
    Onboard Wifi Service (wifi_impt)
    Onboard Dining Service (dining_impt)
    Onboard Entertainment (entertain_impt)
    """
    # Map importance scale
    map_dict = {
        None: np.nan,
        "Not at all important": 1,
        "A little important": 2,
        "Somewhat important": 3,
        "Very important": 4,
        "Extremely important": 5
    }
    cruise = cruise.replace({
        "wifi_impt": map_dict,
        "dining_impt": map_dict,
        "entertain_impt": map_dict
    })

    """
    Cruise Name (cruise)
    """
    # Standardize cruise name
    map_dict = {
        "blast": "Blastoise",
        "blastoise": "Blastoise",
        "blast0ise": "Blastoise",
        "IAPRAS": "Lapras",
        "lap": "Lapras",
        "lapras": "Lapras"
    }
    cruise = cruise.replace({"cruise": map_dict})

    # One-hot encoding
    cruise["cruise_enc"] = cruise["cruise"].astype('category').cat.codes
    enc = OneHotEncoder()
    enc_data = pd.DataFrame(enc.fit_transform(
        cruise[["cruise_enc"]]).toarray())

    # Add encoded columns
    enc_data.columns = ["cruise." + str(i) for i in cruise["cruise"].unique()]
    cruise = cruise.join(enc_data)
    cruise = cruise.drop(["cruise_enc", "cruise.None"], axis="columns")

    """
    Ticket Type (ticket)
    """
    # Map price/prestige scale
    map_dict = {
        None: np.nan,
        "Standard": 1,
        "Deluxe": 2,
        "Luxury": 3
    }
    cruise = cruise.replace({"ticket": map_dict})

    """
    Cruise Distance (distance)
    """
    # Convert distance to km
    cruise["distance_km"] = 0
    for i in cruise.index:
        if str(cruise.loc[i, "distance"]) == "None":
            cruise.loc[i, "distance_km"] = np.nan
        elif "KM" in str(cruise.loc[i, "distance"]):
            cruise.loc[i, "distance_km"] = abs(int(cruise.loc[i, "distance"].split('KM')[0]))
        elif "Miles" in str(cruise.loc[i, "distance"]):
            cruise.loc[i, "distance_km"] = abs(int(cruise.loc[i, "distance"].split('Miles')[0]) * 1.609)
        else:
            print("WARNING: Check index {} for distance.".format(i))
            logging.warning("Check index {} for distance.".format(i))
    cruise = cruise.drop(["distance"], axis="columns")

    """
    Dining (dining_satisfy)
    """
    # Assume Dining to be missing if other cruise_post entries are missing
    cruise["dining_satisfy"] = cruise["dining_satisfy"].astype("float64")
    for i in cruise.index:
        if (cruise.loc[i, "cruise.Blastoise"] == 0) \
                and (cruise.loc[i, "cruise.Lapras"] == 0) \
                and np.isnan(cruise.loc[i, "ticket"]) \
                and np.isnan(cruise.loc[i, "distance_km"]) \
                and np.isnan(cruise.loc[i, "wifi_satisfy"]) \
                and np.isnan(cruise.loc[i, "entertain_satisfy"]):
            cruise.loc[i, "dining_satisfy"] = np.nan

    """
    Embarkation/Disembarkation time convenient (schedule_impt)
    Ease of Online booking (booking_impt)
    Gate location (gate_impt)
    Online Check-in (online_checkin_impt)
    Cabin Comfort (comfort_impt)
    Cabin Service (cabin_svc_impt)
    Baggage Handling (baggage_impt)
    Port Check-in Service (port_checkin_impt)
    Onboard Service (onboard_svc_impt)
    Cleanliness (clean_impt)
    """
    # Extract columns
    float_col = cruise[["schedule_impt", "booking_impt", "gate_impt",
                        "online_checkin_impt", "comfort_impt", "cabin_svc_impt",
                        "baggage_impt", "port_checkin_impt", "onboard_svc_impt", "clean_impt"]]

    # Convert zeroes to NaN
    map_dict = {0: np.nan}
    for col in float_col.columns:
        cruise = cruise.replace({col: map_dict})

    """
    Old columns
    """
    # Remove old columns that are not useful for prediction
    cruise = cruise.drop(["gender", "source_type", "source_traffic", "cruise"], axis="columns")

    return cruise

def transform_cruise(cruise):
    print("Applying transformations...")
    logging.info("Applying transformations...")

    # Log numerical columns to reduce skewness and bimodal distribution
    cruise["age_log"] = np.log(cruise["age"])
    cruise["distance_km_log"] = np.log(cruise["distance_km"])
    cruise = cruise.drop(["age", "distance_km"], axis="columns")

    return cruise

def impute_cruise(cruise):
    print("Data imputation...")
    logging.info("Data imputation...")

    # Create a function to fillna by group
    def fillna_by_group(data, fill_var, group_vars):

        # Calculate median values after grouping
        map_dict = data.groupby(group_vars).median()[fill_var].to_dict()

        # Get median value
        for i in range(len(data)):
            key_list = []
            for key_var in group_vars:
                key = data.loc[i, key_var]
                key_list.append(key)
            key_tuple = tuple(key_list)

            # Replace NaN with median
            if np.isnan(cruise.loc[i, fill_var]):
                if not np.isnan(key_tuple).all():
                    try:
                        data.loc[i, fill_var] = map_dict[key_tuple]
                    except:
                        pass

        # Fill remaining NaN values with overall median of column
        data[fill_var] = data[fill_var].fillna(data[fill_var].median())
        return data

    """
    Missing data columns
    """
    # Drop columns with a significant amount of data missing
    cruise = cruise.drop(["wifi_satisfy", "entertain_satisfy"], axis="columns")

    """
    Numerical variables
    """
    # Fill numerical variables with median
    cruise_num = cruise[["age_log", "distance_km_log"]]
    cruise[cruise_num.columns] = cruise_num.fillna(cruise_num.median())

    """
    Categorical variables
    """

    # booking_impt, wifi_impt, gate_impt, schedule_impt
    cruise = fillna_by_group(cruise, "booking_impt", ["wifi_impt", "gate_impt", "schedule_impt"])
    cruise = fillna_by_group(cruise, "wifi_impt", ["booking_impt", "gate_impt", "schedule_impt"])
    cruise = fillna_by_group(cruise, "gate_impt", ["booking_impt", "wifi_impt", "schedule_impt"])
    cruise = fillna_by_group(cruise, "schedule_impt", ["booking_impt", "wifi_impt", "gate_impt"])

    # comfort_impt, dining_impt, entertain_impt, clean_impt
    cruise = fillna_by_group(cruise, "comfort_impt", ["dining_impt", "entertain_impt", "clean_impt"])
    cruise = fillna_by_group(cruise, "dining_impt", ["comfort_impt", "entertain_impt", "clean_impt"])
    cruise = fillna_by_group(cruise, "entertain_impt", ["comfort_impt", "dining_impt", "clean_impt"])
    cruise = fillna_by_group(cruise, "clean_impt", ["comfort_impt", "dining_impt", "entertain_impt"])

    # baggage_impt, cabin_svc_impt, onboard_svc_impt
    cruise = fillna_by_group(cruise, "baggage_impt", ["cabin_svc_impt", "onboard_svc_impt"])
    cruise = fillna_by_group(cruise, "cabin_svc_impt", ["baggage_impt", "onboard_svc_impt"])
    cruise = fillna_by_group(cruise, "onboard_svc_impt", ["baggage_impt", "cabin_svc_impt"])

    # cruise.Blastoise, source_type.Direct, source_traffic.CompanyWebsite,
    # source_traffic.EmailMarketing, online_checkin_impt, ticket
    cruise = fillna_by_group(cruise, "online_checkin_impt", ["cruise.Blastoise",
                                                             "source_type.Direct",
                                                             "source_traffic.CompanyWebsite",
                                                             "source_traffic.EmailMarketing",
                                                             "ticket"])
    cruise = fillna_by_group(cruise, "ticket", ["cruise.Blastoise",
                                                "source_type.Direct",
                                                "source_traffic.CompanyWebsite",
                                                "source_traffic.EmailMarketing",
                                                "online_checkin_impt"])

    # Independent variables
    cruise["port_checkin_impt"] = cruise["port_checkin_impt"].fillna(cruise["port_checkin_impt"].median())
    cruise["dining_satisfy"] = cruise["dining_satisfy"].fillna(cruise["dining_satisfy"].median())

    return cruise


"""
Main
"""
if __name__ == '__main__':

    # Set directory
    in_dir = "data"

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename=os.path.join("output", "preprocessing.log")
    )

    # Preprocessing
    data = load_cruise_data(in_dir)  # Load data
    data = rename_cruise_col(data)  # Rename columns
    data = remove_cruise_duplicates(data)  # Remove duplicates
    data = cruise_ft_eng(data)  # Feature engineering
    data = transform_cruise(data)  # Apply transformations
    data = impute_cruise(data)  # Data imputation

    # Save preprocessed data
    print("Saving preprocessed data...")
    logging.info("Saving preprocessed data...")
    if not os.path.exists("output"):
        os.mkdir("output")
    data.to_csv(os.path.join("output", "preprocessed.csv"), index=False)

    print("Completed!")
    logging.info("Completed!")
    logging.shutdown()
