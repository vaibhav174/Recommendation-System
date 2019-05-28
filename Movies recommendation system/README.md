# Movies-recommendation-system
Recommendation Systems using Machine Learning

## extract2.py
The data is extracted from CSV files. The following tables are formed:

### Movies

Attributes:

- id: Movie id
- name: Movie name
- rating: Average rating of that movie

Snapshot of data:

| id    | name                  | rating    |
|-------|-----------------------|-----------|
| 2959  | Fight Club (1999)     | 4.17822   |
| 48780 | Prestige, The (2006)  | 4.125     |
| 74458 | Shutter Island (2010) | 3.97412   |
| ...   | ...                   | ...       |

### Genres

Attributes:

- id: Genre id
- name: Genre name

Snapshot of data:

| id    | name      |
|-------|-----------|
| 1     | Mystery   |
| 2     | Drama     |
| 19    | Thriller  |
| ...   | ...       |

### Movies_Genres

Attributes:

- movie_id: movie id
- genre_id: genre id

Snapshot of data:

| movie_id  | genre_id  |
|-----------|-----------|
| 2959      | 14        |
| 2959      | 7         |
| 2959      | 2         |
| 2959      | 19        |
| 48780     | 2         |
| 48780     | 1         |
| 48780     | 4         |
| 48780     | 19        |
| ...       | ...       |


### Ratings

Attributes:

- user_id: id of the user who has rated the movies
- movie_id: id of the movie that the user has rated
- rating: rating given by `user_id` to `movie_id`

Snapshot of data:

| user_id   | movie_id  | rating    |
|-----------|-----------|-----------|
| 1         | 31        | 2.5       |
| 1         | 1029      | 3.0       |
| 2         | 17        | 5.0       |
| ...       | ...       | ...       |


## content.py

This is the content based filtering approach. The following things are done:

1. Get a list of favourite movies from the user.
2. Get the ratings of all the movies liked by the user.
3. Make an exhaustive Genre set that encompasses all the favourite movies.
4. Build a movie list that has those genres. Sort the movies in such a way that the movie with most genre match will be on top.
5. Get the top 50 movies from the above list and apply k-NN to get top `k` movies.
6. Present the names of the `k` movies in the end result.

Content based filtering works by first getting the items the target user is interested in. For each of these item, we find other items that have similar characterstics. An exhaustive list of all such items is created. In our case, we first ask the user for his/her favorite movies. Based on these obtain the following data from the database:

- Average rating of all the movies in favorites list.
- All the genres of all the movies in favorites list.

After we have all the genres that the target user is interested in, we will get all the movies that fall in any of those genres. Let's assume that the set of genres that the user is interested in is `A`. For all the movies extracted in this step, find out the genres of each of that movie. Let's name this set B. Now, we will sort the list in descending order such that the movie with `A intersection B` value will be on top.

After we have this sorted data, we will extract a few top movies, say 50. This data will be used to apply k-NN algorithm to solve this problem. The training data will be the rating of the rating of the user's favorite movies. The testing data will be the top 50 movies extracted from the database. The top `k` movies found closest to the movies rated by the user will be recommended to the target user.


## coll.py

This is the collaborative based filtering approach. Collaborative filtering works by using the data of users who have similar interests as that of tha target user. If the similarity is high, then we can assume that their interests are almost same and thus the user can be used to give recommendations to the target user.

We have used Pearson's Coefficient formula in our project. To illustrate its use let's take the following example. Assume we have `n` users `A_1, A_2, A_3, ..., A_n`. Each of these users have seen some movies and rated them. According to the description provided in the dataset, each user has rated atleast 20 movies.

Let's take 2 users - X and Y. We need to calculate the Pearson's coefficient for these two users to understand how much the data is correlated. For this, we will first have to extract the set of common movies seen and rated by both X and Y. This will be `X intersection Y`. For any movie in `X intersection Y`, we have the rating of both X and Y. Now, we will calculate the Pearson's Coefficient using the following formula:

![formula1](http://latex.codecogs.com/gif.latex?r%28X%2C%20Y%29%20%3D%20%5Cfrac%7B%5Csum_k%28X_k-%5Cbar%7BX%7D%29%28Y_k-%5Cbar%7BY%7D%29%7D%7B%5Csqrt%7B%5Csum_k%28X_k-%5Cbar%7BX%7D%29%5E2%5Csum_k%28Y_k-%5Cbar%7BY%7D%29%5E2%7D%7D)

Here,

- ![r(X, Y)](http://latex.codecogs.com/gif.latex?r%28X%2C%20Y%29) - Pearson's Coefficient between `X` and `Y`
- ![X_k, Y_k](http://latex.codecogs.com/gif.latex?X_k%2C%20Y_k) - The ratings of item `k` by `X` and `Y`
- ![X_bar, Y_bar](http://latex.codecogs.com/gif.latex?%5Cbar%7BX%7D%2C%20%5Cbar%7BY%7D) - mean values of ratings of `X` and `Y`

After calculating the Pearson's coefficient of the target user with respect to all the other users, we will store this data in some internal data structure. The following points are to be noted:

- The users for which r(X, Y) belongs to the range [-1, 0.2] are ignored (we have no use of negative correlations or little correlations).
- Those users are ignored for which `X intersection Y` < 5, as there is no substantial data to support correlation (it can occur by chance).

After this, we will consider a few top results (i.e., the users for which there is substantial correlation and a high intersection value). An exhaustive list of movies is created which is not seen by the target user and a prediction rating for all those movies is calculated using the following formula:

![formula2](http://latex.codecogs.com/gif.latex?p%28X_i%29%20%3D%20%5Cfrac%7B%5Csum_k%20Y_i%20-%20r%28X%2C%20Y%29%7D%7Bn%7D)

Here,
- ![p(X_i)](http://latex.codecogs.com/gif.latex?p%28X_i%29) - this is the predicted rating of item `i` for user `X`
- ![Y, n](http://latex.codecogs.com/gif.latex?Y%2C%20n) - `Y` consists of all the `n` people who have rated `i`

In this way a final list is created which stored the movie_id and their predicted ratings for the target user. This list is sorted in descending order with respect to predicted ratings and the top few results are displayed.


## hybrid.py

This is the Hybrid Filtering approach which is an amalgamation of both Collaborative and Content based filtering approach. Hybrid approach is more dynamic and provides better results than the case when both the other approaches are applied individually. It tries to make up for the deficiencies of one method with the use of the other.

This approach works as follows:

- First we apply the Collaborative filtering approach, to find the users with which the target user is highly correlated.
- We find out the exhaustive genre set that encompasses all the movies rated by the target user.
- After we find the correlated users, we find out the movies that are seen by those users but not seen by the target user.
- This data is stored in a data structure. It will contain `movies_id`, `rating` and `genre_match_with_target_user`.
- Top few results are used and applies in k-NN just like in Content Based filtering approach.
- Final results are displayed.
