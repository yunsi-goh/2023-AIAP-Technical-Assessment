# General parameters
test_size = 0.3
random_state = 42

# Random forest parameters
RF_params = {
    'n_estimators': [100, 200, 500, 1000],
    'max_depth': [None, 2, 5, 10],
    'max_features': ['sqrt', 'log2'],
    'random_state': [random_state]
}

# Support vector machine parameters
SVM_params = {
    'C': [1e-1, 1e-0, 1e1],
    'gamma': [1e-1, 1e-0, 1e1],
    'kernel': ['rbf', 'poly', 'linear'],
    'random_state': [random_state]
}

# Support vector machine parameters
KNN_params = {
    'n_neighbors': [5, 10, 20, 50],
    'weights': ['uniform', 'distance'],
    'metric': ['minkowski', 'euclidean', 'manhattan']
}

# Others
rename_columns = {
    "gender": "Gender",
    "gender.Male": "Gender - Male",
    "gender.Female": "Gender - Female",
    "birth_date": "Date of Birth",
    "age": "Age",
    "age_log": "Age (log-transformed)",
    "source": "Source of Traffic",
    "source_type.Direct": "Source of Traffic - Direct",
    "source_type.Indirect": "Source of Traffic - Indirect",
    "source_traffic.CompanyWebsite": "Source of Traffic - Direct - Company Website",
    "source_traffic.EmailMarketing": "Source of Traffic - Direct - Email Marketing",
    "source_traffic.SocialMedia": "Source of Traffic - Indirect - Social Media",
    "source_traffic.SearchEngine": "Source of Traffic - Indirect - Search Engine",
    "wifi_impt": "Onboard Wifi Service",
    "schedule_impt": "Embarkation/Disembarkation time convenient",
    "booking_impt": "Ease of Online booking",
    "gate_impt": "Gate location",
    "log_time": "Logging",
    "dining_impt": "Onboard Dining Service",
    "online_checkin_impt": "Online Check-in",
    "comfort_impt": "Cabin Comfort",
    "entertain_impt": "Onboard Entertainment",
    "cabin_svc_impt": "Cabin service",
    "baggage_impt": "Baggage handling",
    "port_checkin_impt": "Port Check-in Service",
    "onboard_svc_impt": "Onboard Service",
    "clean_impt": "Cleanliness",
    "cruise": "Cruise Name",
    "cruise.Blastoise": "Cruise Name - Blastoise",
    "cruise.Lapras": "Cruise Name - Lapras",
    "ticket": "Ticket Type",
    "distance": "Cruise Distance",
    "distance_km": "Cruise Distance (km)",
    "distance_km_log": "Cruise Distance (km, log-transformed)",
    "wifi_satisfy": "WiFi",
    "dining_satisfy": "Dining",
    "entertain_satisfy": "Entertainment"
}
