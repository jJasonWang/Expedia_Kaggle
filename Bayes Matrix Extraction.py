#### This code generates the bayes probability matrix for all categorical variable.

import pandas as pd
import numpy as np
import pickle as pk

train = pd.read_csv('train.csv')

## For categorical data

Column_names = ["site_name", "posa_continent", "user_location_country",
				"user_location_region", "user_location_city","is_mobile",
				"is_package", "channel", "srch_adults_cnt", "srch_children_cnt", 
				"srch_rm_cnt", "srch_destination_id", "srch_destination_type_id",
				"hotel_continent", "hotel_country", "hotel_market", "hotel_cluster"]

for name in Column_names:
	train_col = train[name]
	matrix_col = np.unique(train_col)

	map_to_matrix = {}
	for i in range(len(matrix_col)):
		map_to_matrix[matrix_col[i]] = i

	hotel_cluster = train['hotel_cluster']
	hotel_matrix = np.unique(hotel_cluster)

	matrix = np.zeros((len(matrix_col), len(hotel_matrix)))

	for i in range(train.shape[0]):
		matrix[map_to_matrix[train_col[i]],hotel_cluster[i]] += 1

	np.save(name, matrix)
	pk.dump(map_to_matrix, open(name+'.p', "wb" ) )
	print name

is_booking = train['is_booking']

hotel_cluster = train['hotel_cluster']
hotel_matrix = np.unique(hotel_cluster)

for name in Column_names:
	train_col = train[name]
	matrix_col = np.unique(train_col)

	map_to_matrix = pickle.load( open( name+".p", "rb" ) )

	matrix = np.zeros((len(matrix_col), len(hotel_matrix)))

	for i in range(train.shape[0]):
		if is_booking[i] == 1:
			matrix[map_to_matrix[train_col[i]],hotel_cluster[i]] += 1

	np.save(name+'_book', matrix)
	print name

###### date_time
name = 'date_time'
train_col = train[name]
train_col = [int(i.split('-')[1])-1 for i in train_col]
matrix_col = np.unique(train_col)

map_to_matrix = {}
for i in range(len(matrix_col)):
	map_to_matrix[matrix_col[i]] = i

is_booking = train['is_booking']

hotel_cluster = train['hotel_cluster']
hotel_matrix = np.unique(hotel_cluster)

matrix = np.zeros((len(matrix_col), len(hotel_matrix)))
matrix_book = np.zeros((len(matrix_col), len(hotel_matrix)))

for i in range(train.shape[0]):
	matrix[map_to_matrix[train_col[i]],hotel_cluster[i]] += 1
	if is_booking[i] == 1:
		matrix_book[map_to_matrix[train_col[i]],hotel_cluster[i]] += 1

np.save(name, matrix)
pk.dump(map_to_matrix, open(name+'.p', "wb" ) )
np.save(name+'_book', matrix_book)
print name

###### orig_destination_distance 
name = 'orig_destination_distance'
train_col = train[name]

import math
from scipy.stats.mstats import mquantiles

non_na_train_col = [number for number in train_col if not math.isnan(number)]
boundary = mquantiles(non_na_train_col, np.asarray(range(100))*0.01+0.01)

matrix_col = range(100)
matrix_col.append('nan')

map_to_matrix = {}
for i in range(len(matrix_col)):
	map_to_matrix[matrix_col[i]] = i


train_col_tmp = []

matrix = np.zeros((len(matrix_col), len(hotel_matrix)))
matrix_book = np.zeros((len(matrix_col), len(hotel_matrix)))

for i in range(len(train_col)):
	if math.isnan(train_col[i]):
		train_col_tmp.append('nan')
	else:
		train_col_tmp.append(np.sum(train_col[i] > boundary))

	matrix[map_to_matrix[train_col_tmp[-1]],hotel_cluster[i]] += 1
	if is_booking[i] == 1:
		matrix_book[map_to_matrix[train_col_tmp[-1]],hotel_cluster[i]] += 1

	if (i % 1000000 == 0):
		print i

np.save(name, matrix)
pk.dump(map_to_matrix, open(name+'.p', "wb" ) )
np.save(name+'_book', matrix_book)
np.save(name+'_boundary', boundary)



