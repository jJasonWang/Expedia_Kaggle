import numpy as np
import pandas as pd

# All the column names
all_cols = ["date_time", "site_name", "posa_continent", "user_location_country", 
            "user_location_region", "user_location_city",  "orig_destination_distance",
            "user_id", "is_mobile", "is_package", "channel", "srch_ci", 
            "srch_co", "srch_adults_cnt", "srch_children_cnt", "srch_rm_cnt", 
            "srch_destination_id", "srch_destination_type_id", "is_booking", "cnt", 
            "hotel_continent", "hotel_country", "hotel_market", "hotel_cluster"]

expedia_train = pd.DataFrame(columns=all_cols)
expedia_train_chunk = pd.read_csv('Data/train.csv', chunksize=100000)

# Process the data by chunks and filter out data with is_booking = 0
for chunk in expedia_train_chunk:
    expedia_train = pd.concat([expedia_train, chunk[chunk['is_booking'] == 1][all_cols]])

# Transform the y into calculable format
user_hotel = dict()
for i in range(len(expedia_train)):
    user_id = expedia_train['user_id'].iloc[i]
    hotel_cluster = expedia_train.iloc[i, -1]
    if user_hotel.get(user_id, 0) == 0:
        user_hotel[user_id] = [hotel_cluster]
    else:
        user_hotel[user_id].append(hotel_cluster)

user_hotel = dict([(key, list(set(item))) for key, item in user_hotel.items()])

# use pickle to save it
pickle.dump(user_hotel, open("user_hotel.p", "wb"))

# read in the dictionary again
user_hotel = pickle.load(open("user_hotel.p", "rb"))