import sqlite3
from sklearn.neighbors import NearestNeighbors
import numpy as np

# get input from the user: first the number of movies
# then id of all the movies
mov_no = int(input('Enter the number of movies: '))
print ('Movie id in separated lines: ')
mov_id, mov_rate = [None]*mov_no, [None]*mov_no
for i in range(mov_no):
    # mov_id[i], mov_rate[i] = map(int, raw_input().split())
    mov_id[i] = int(input())

# connect with the database
# conn = sqlite3.connect('moviesdb2.sqlite')
with sqlite3.connect('moviesdb2.sqlite') as conn:
    cur = conn.cursor()

    # get the rating of all the movies liked by user from the database
    for i in range(mov_no):
        mov_rate[i] = cur.execute('''
            SELECT rating FROM Movies WHERE id = (?)''',
             (mov_id[i], )).fetchone()[0]

    # make a set of all the distinct genres from all of the entered movies
    genre_set = set()
    for i in range(mov_no):
        temp = cur.execute('''
            SELECT genre_id FROM Movies_Genres WHERE movie_id = (?)''',
            (mov_id[i], )).fetchall()
        for value in temp:
            genre_set.add(value[0])

    print(genre_set)

    # Make a temporary movie_set by extracting all the movies for each of the
    # genres extracted above
    temp_movie_set = set()
    genre_list = sorted(list(genre_set))
    for i in range(len(genre_list)):
        temp = cur.execute('''
            SELECT movie_id FROM Movies_Genres WHERE genre_id = (?)''',
            (genre_list[i], )).fetchall()
        for value in temp:
            if value[0] not in mov_id:
                temp_movie_set.add(value[0])

    temp_movie_list = list(temp_movie_set)
    # print movie_list

    # Make another tempprary_movie_list2 where each element is a tuple.
    # The first element of the tuple will store the movie id and the second
    # element will store the value of intersection of the genres of that movie
    # and the genres extracted above (that the user likes)
    temp_movie_list2 = []
    for mov in temp_movie_list:
        temp = cur.execute('''
            SELECT genre_id FROM Movies_Genres WHERE movie_id = (?)''',
            (mov, )).fetchall()
        temp = [value[0] for value in temp]
        temp_movie_list2.append((mov, len(set(temp).intersection(genre_list)), ))

    def cmp(a):
        return a[-1]

    temp_movie_list2 = sorted(temp_movie_list2, key=cmp, reverse=True)

    # Extract the top 50 movies with high "genre match" value
    temp_movie_list2 = temp_movie_list2[:50]
    movie_list = []
    for mov in temp_movie_list2:
        cur.execute('SELECT rating FROM Movies WHERE id = (?)', (mov[0], ))
        movie_list.append((mov[0], cur.fetchone()[0], ))

    for item in movie_list:
        print(item)

    # create a training dataset and find the k nearest neighbors among the
    # above 50 movies.
    training_data = [[item[1]] for item in movie_list]
    train = np.array(training_data)
    nbrs = NearestNeighbors()
    nbrs.fit(train)
    indices = nbrs.kneighbors([[item] for item in mov_rate],
        n_neighbors=7, return_distance=False)

    print(indices)

    # print the names of all the recommended movies
    for value in indices[0]:
        # print movie_list[value]
        temp = cur.execute('''
            SELECT movie FROM Movies WHERE id = (?)''',
            (movie_list[value][0], )).fetchone()[0]
        print(temp)
