import sqlite3

n = int(raw_input('Enter the number of friends: '))
friends_list = [None]*n
for i in xrange(n):
    idd = int(raw_input())
    friends_list[i] = idd

friends_data = []

# connect with the database.
conn = sqlite3.connect('moviesdb.sqlite')
cur = conn.cursor()

# get all the movies rated by each of the friends.
for friend in friends_list:
    cur.execute('''
        SELECT user_id, movie_id, rating FROM Ratings WHERE user_id = (?)''',
        (friend, )
    )
    temp_data = cur.fetchall()
    # append all the data of each friend to the main "friends_data".
    for value in temp_data:
        friends_data.append(value)
"""
for value in friends_data:
    print value
"""

n = int(raw_input('Enter the number of genres: '))
genres_list = set()
for i in xrange(n):
    idd = int(raw_input())
    genres_list.add(idd)

# check all the matching genres of friends_data with that of
for i in xrange(len(friends_data)):
    item = friends_data[i]
    cur.execute('''
        SELECT genre_id from Movies_Genres WHERE movie_id = (?)''',
        (item[1], )
    )
    temp_genres = cur.fetchall()
    temp_genres = [j[0] for j in temp_genres]
    correlation = len(genres_list.intersection(temp_genres))
    friends_data[i] = (item[0], item[1], item[2], correlation, )


def func(a):
    return (a[-1], a[-2], )

friends_data = sorted(friends_data, key=func, reverse=True)

"""
for item in friends_data:
    print item
"""

movies = set()

r = int(raw_input('Enter the number of recommendations that you need: \n'))
i = 0
while i < len(friends_data) and len(movies) < r:
    cur.execute('''
        SELECT name FROM Movies WHERE id = (?)''', (friends_data[i][1], ))
    movie = cur.fetchall()
    movies.add(str(movie[0][0]))
    i += 1

print 'You should check out the following movies: \n\n\n'
for movie in movies:
    print movie
