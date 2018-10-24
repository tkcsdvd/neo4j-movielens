# MovieLens in Neo4j

Load MovieLens dataset into Neo4j and provide an API to retrieve data.

![](https://i.imgur.com/uHgJsHp.png)

## Table of contents

 * [Stack](#stack)
 * [Project structure](#project-structure)
 * [Data](#data)
 * [Graph Structure](#graph-structure)
 * [Ingestion](#ingestion)
 * [API](#api)
 * [Docker](#docker)
 * [Recommender Enginer](#recommender-engine)


## Stack

 * python 3.7
 * py2neo
 * neo4j
 * flask
 * swagger
 * connexion

## Project structure

```
├── api/
│   │── swagger/
│   │   └── swagger.yml
│   └── movielens-app.py│
│      
├── docker/
│   └── ...
│
├── ingestion/
│   │── data/
│   │   │── links.csv
│   │   │── movies.csv
│   │   │── ratings.csv
│   │   └── tags.csv
│   │── test/
│   │   └── ingestion_tests.py
│   └── ingestion.py
│
└── README.md
```


## Data

MovieLens 20M Dataset

20 million ratings and 465,000 tag applications applied to 27,000 movies by 138,000 users. 


##### Ratings Data File Structure (ratings.csv)

All ratings are contained in the file `ratings.csv`. Each line of this file after the header row represents one rating of one movie by one user, and has the following format:

    userId,movieId,rating,timestamp
    
##### Tags Data File Structure (tags.csv)

All tags are contained in the file `tags.csv`. Each line of this file after the header row represents one tag applied to one movie by one user, and has the following format:

    userId,movieId,tag,timestamp

##### Movies Data File Structure (movies.csv)

Movie information is contained in the file `movies.csv`. Each line of this file after the header row represents one movie, and has the following format:

    movieId,title,genres
    
##### Links Data File Structure (links.csv)

Identifiers that can be used to link to other sources of movie data are contained in the file `links.csv`. Each line of this file after the header row represents one movie, and has the following format:

    movieId,imdbId,tmdbId
    
## Graph Structure

The graph structures consists of nodes with 3 distinct *labels* (**Genre**, **Movie**, **User**), 3 *relationships* (**RATED**, **TAGGED**, **IS_GENRE_OF**). Links are added as additional *properties* to movie nodes.

![](https://i.imgur.com/PW1GohY.png "Logo Title Text 1")

## Ingestion

Python script (*ingestion.py*) that loads MovieLens dataset into Neo4j in a graph structure.

#### Steps

 * Create **Genre** nodes
 * Load *movies.csv* 
    * Create **Movie** nodes
    * Create Movie-Genre relationships
 * Load *ratings.csv*
    * Create **User** nodes
    * Create User-Movie **rating** relationships
 * Load *tags.csv*
    * Create User-Movie **tag** relationships
 * Load *links.csv*
    * Update Movie nodes properties with links

## API

#### Description

API documentation is generated using *Swagger* and *Connexion*.

One example: 

**/api/movie/ratings/[TITLE]**

Returns the ratings submitted for a given movie. 

http://localhost:5000/api/movie/ratings/Braveheart

will return:

```
[
  {
    "rating": 4.0, 
    "user": "User 1"
  }, 
  {
    "rating": 4.0, 
    "user": "User 5"
  }, 
  {
    "rating": 5.0, 
    "user": "User 6"
  }
]
```

#### Documentation

When docker compose up is finished go to http://localhost:5000/api/ui to see the full documentation.

![](https://i.imgur.com/4MaEl2w.png)


## Docker

##### Instructions
 
 * *cd* into folder
 * run ``` docker-compose up ```
 * wait for ingestion to finish
 
    <img src="https://i.imgur.com/AoPs8hE.png" width="400">

 * open Neo4j UI at http://localhost:7474
 * open API documentation at http://localhost:5000/api/ui
 


**For the Docker solution the MovieLens version with 100K ratings was used**

If you want to use the 20M dataset:

 * download dataset from http://files.grouplens.org/datasets/movielens/ml-20m.zip 
 * move unzipped data into *docker/ingestion/data*
 * then follow instructions above
 
**By default it only loads 1000 movies/links/ratings/tags.**

If you want to increase that, you can do so by changing *ingestion.py*:

```python
N_MOVIES = 1000
N_RATINGS = 1000
N_TAGS = 1000
N_LINKS = 1000
```

If only a subset is used, some relationships might not be created due to missing nodes.
 
##### Structure

```
docker/
├── api/
│   │── swagger/
│   │   └── swagger.yml
│   │── Dockerfile
│   │── movielens-app.py
│   └── requirements.txt
│      
├── ingestion/
│   │── data/
│   │   │── links.csv
│   │   │── movies.csv
│   │   │── ratings.csv
│   │   └── tags.csv
│   │── Dockerfile
│   │── ingestion.py
│   └── requirements.tx
│
└── docker-compose.yml
```


## Recommender Engine

Based on: http://guides.neo4j.com/sandbox/recommendations

##### Content-based

Recommend top *N* movies for a given movie, based on common genres.

```/api/rec_engine/content/[TITLE]/[N]```

**Example:**

Top 3 movies similar to *Braveheart*.

http://localhost:5000/api/rec_engine/content/Braveheart/3

Returns:

```
[
  {
    "genres": [
      "Action", 
      "Drama", 
      "War"
    ], 
    "numberOfSharedGenres": 3, 
    "title": "Courage Under Fire"
  }, 
  {
    "genres": [
      "Action", 
      "Drama", 
      "War"
    ], 
    "numberOfSharedGenres": 3, 
    "title": "Great Escape, The"
  }, 
  {
    "genres": [
      "Action", 
      "Drama", 
      "War"
    ], 
    "numberOfSharedGenres": 3, 
    "title": "Henry V"
  }
]
```

Cypher query:

```cypher
MATCH (m:Movie)<-[:IS_GENRE_OF]-(g:Genre)-[:IS_GENRE_OF]->(rec:Movie)
WHERE m.title = [TITLE]
WITH rec, COLLECT(g.name) AS genres, COUNT(*) AS sharedGenres
RETURN rec.title as title, genres, sharedGenres
ORDER BY sharedGenres DESC LIMIT [N];
```

#### Collaborative Filtering

Recommend top *N* movies for a given user, based on collaborative filtering. For this to work properly much more than 1000 ratings should be loaded.

```/api/rec_engine/collab/[USER_ID]/[N]```

**Example:**

For *User 1* return top *5* movies.

http://localhost:5000/api/rec_engine/collab/User%201/5

Returns:

```
[
  {
    "score": 2.7610991022551645, 
    "title": "Eat Drink Man Woman (Yin shi nan nu)"
  }, 
  {
    "score": 2.1133083447185044, 
    "title": "Heavenly Creatures"
  }, 
  {
    "score": 2.0585623586160793, 
    "title": "Living in Oblivion"
  }, 
  {
    "score": 2.0585623586160793, 
    "title": "Notorious"
  }, 
  {
    "score": 2.0585623586160793, 
    "title": "High Noon"
  }
]
```
Cypher query:

```
MATCH (u1:User {id:[USER_ID]})-[r:RATED]->(m:Movie)
WITH u1, avg(r.rating) AS u1_mean

MATCH (u1)-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2)
WITH u1, u1_mean, u2, COLLECT({r1: r1, r2: r2}) AS ratings WHERE size(ratings) > 10

MATCH (u2)-[r:RATED]->(m:Movie)
WITH u1, u1_mean, u2, avg(r.rating) AS u2_mean, ratings

UNWIND ratings AS r

WITH sum( (r.r1.rating-u1_mean) * (r.r2.rating-u2_mean) ) AS nom,
     sqrt( sum( (r.r1.rating - u1_mean)^2) * sum( (r.r2.rating - u2_mean) ^2)) AS denom,
     u1, u2 WHERE denom <> 0

WITH u1, u2, nom/denom AS pearson
ORDER BY pearson DESC LIMIT 10

MATCH (u2)-[r:RATED]->(m:Movie) WHERE NOT EXISTS( (u1)-[:RATED]->(m) )

RETURN m.title, SUM( pearson * r.rating) AS score
ORDER BY score DESC LIMIT [N]
```