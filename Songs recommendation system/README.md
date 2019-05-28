# Songs-recommendation-system

It recommend songs using 3 different algorithms.
1) Popularity based recommendation
2) Nearest neighbour
3) Matrix factorization

## DATA

Data used is a subset of the Million Songs Dataset.
Source : http://labrosa.ee.columbia.edu/millionsong/ 
Its subset link can be found within the project.

Snapshot of data:

| user_id	|                   song_id                                     |count|	    title     |	artist_name  |	year |
|---------|---------------------------------------------------------------|-----|---------------|--------------|-------|
|    0	  |  b80344d063b5ccb3212f76538f3d9e43d87dca9e	SOAKIMP12A8C130995  |  1	|   The Cove    |	Jack Johnson |	0    | 
|    1	  |  b80344d063b5ccb3212f76538f3d9e43d87dca9e	SOBBMDR12A8C13253B	|  2	|Entre Dos Aguas|	Paco De Lucia|	1976 |
|    2	  |  b80344d063b5ccb3212f76538f3d9e43d87dca9e	SOBXHDL12A81C204C0	|	 1  |   Stronger    |	 Kanye West  |	2007 |
|    3 	  |  b80344d063b5ccb3212f76538f3d9e43d87dca9e	SOBYHAJ12A6701BF1D	|	 1  |Constellations |	Jack Johnson |	2005 |


## Popularity based

Easiest way to build a recommendation system is popularity based, simply over all the songs that are popular, So how to identify popular songs, which could be identified by which are all the songs that are listened most,

Count feild in the dataset stores how many times user has listen to the song. We can use this feild to determine how much the song is listened by users by adding the the count feilds of a perticular song.This data determines the most popular songs which are recommended to the user.

## Nearest neighbour

It is a type of collaborative filtering models which are based on assumption that people like things similar to other things they like, and things that are liked by other people with similar taste.

In these type of recommendation systems are recommending based on nearest neighbors, nearest neighbor approach used to find out either similar users or similar products,

It can be looked at two ways,

i.User based filtering
ii.Item based filtering

### User-based collaborative filtering:

Find the users who have similar taste of songs as the current user , similarity is based on listening behavior of the user, so based on the neighbor listening behavior we can recommend songs to the current user.

### Item-based collaborative filtering :

Recommend songs that are similar to the songs user listen,similarity is based on co-occurrences of listened songs.

## Matrix factorization

It is also a type of collaborative filtering model. It is basically model based collaborative filtering and matrix factorization is the important technique in recommendation system.

 The intuition behind using matrix factorization to solve this problem is that there should be some latent features that determine how a user listen a song. For example, two users would  often listen a certain song many times. if they both like the singer of the song, or if the song is an romantic song, which is a genre preferred by both users. Hence, if we can discover these latent features, we should be able to predict a song with respect to a certain user, because the features associated with the user should match with the features associated with the song.

