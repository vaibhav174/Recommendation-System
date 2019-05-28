import sqlite3
import numpy as np
from sklearn.neighbors import NearestNeighbors

movie_rating_dict = {}
conn = sqlite3.connect('moviesdb.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Ratings')
db_data = cur.fetchall()

for data in db_data:
    if data[1] not in movie_rating_dict:
        movie_rating_dict[data[1]] = []
    movie_rating_dict[data[1]].append(data[2])

average_movie_rating = []
for key, value in movie_rating_dict.items():
    average_movie_rating.append((key, sum(value)/float(len(value)), ))

average_movie_rating = sorted(average_movie_rating)
for value in average_movie_rating:
    print value

training_data = [[value[1]] for value in average_movie_rating]
train = np.array(training_data)
nbrs = NearestNeighbors(n_neighbors=1)
nbrs.fit(train)
indices = nbrs.kneighbors([[4.66]], return_distance=False)

print '---------------'
for index in indices:
    for value in index:
        print average_movie_rating[value]

cur.execute('''
    SELECT name FROM Movies where id = (?)''', (indices[0][0], ))
temp = cur.fetchall()
print temp
