import csv
import numpy as np

def wtc_loc_from_csv(filename='blob/wtc_loc.csv'):
    data = []
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        for k, row in enumerate(reader):
            data.append(row)
    return np.array(data, dtype=np.single)
