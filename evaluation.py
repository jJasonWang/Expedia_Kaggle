# For true_dict, get the user_hotel by user_hotel = pickle.load(open("user_hotel.p", "rb"))
def evaluation(true_dict, prediction, k=5):
    actuals = []
    preds = []
    for _, p in enumerate(prediction):
        try:
            true_value = true_dict[p[0]]
            pred = [float(h) for h in p[1].split(' ')]
            actuals.append(true_value)
            preds.append(pred)
        except:
            next
    
    return(mapk(actuals, preds, k))

# My example:
# user_hotel
## {5.0: [41.0],
##  7.0: [5.0],
##  8.0: [91.0],
##  9.0: [87.0],
##  11.0: [73.0, 91.0, 68.0, 45.0], ...

#  hotel2[:5]
## [[0, '63 25 52 11 64'],
##  [1, '63 75 30 62 15'],
##  [2, '71 54 56 70 0'],
##  [3, '45 1 24 88 79'],
##  [4, '56 52 39 65 98']]

#  evaluation(user_hotel, hotel2)
## 0.029880987328147167

# Function finds those bad performance points
def find_worse(true_dict, prediction, threshold, k=5):
    apks = np.zeros(len(prediction))
    for i, p in enumerate(prediction):
        try:
            apks[i] = apk(true_dict[p[0]], [float(h) for h in p[1].split(' ')])
        except:
            apks[i] = 1
        
    return(apks < threshold)

# Function create the new sample index
def create_index(X, apks):
    med = np.median(apks); index = []
    
    for i, apk in enumerate(apks):
        if apk > med:
            if np.random.choice([True, False]):
                index.append(i)
        else:
            if np.random.choice([True, False]):
                # If True, double the records
                index.append(i)
                index.append(i)
            else:
                # If False, only one record
                index.append(i)
    
    return(np.asarray(index))