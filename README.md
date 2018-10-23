# MovieLens in Neo4j

Load MovieLens dataset in a graph structure into Neo4j and provide an API to retrieve data.

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
│   │── ingestion/
│   │   │── Dockerfile
│   │   │── ingestion.py
│   │   └── requirements.txt
│   └── docker-compose.yml
│
├── ingestion/
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

![alt text](https://i.imgur.com/PW1GohY.png "Logo Title Text 1")

## Ingestion

## API

##### Description

##### Documentation

![alt text](https://i.imgur.com/4MaEl2w.png)


## Docker

##### Instructions
 
 * *cd* into folder
 * run ``` docker-compose up ```
 * wait for ingestion to finish
 
    <img src="https://i.imgur.com/AoPs8hE.png" width="300">

 * open Neo4j UI at http://localhost:7474
 * open API documentation at http://localhost/api/ui
 


**For the Docker solution the MovieLens version with 100K ratings was used**

If you want to use the 20M dataset:

 * download dataset from http://files.grouplens.org/datasets/movielens/ml-20m.zip 
 * move unzipped data into docker/ingestion/data
 * then follow instructions above
 
**By default it only loads 1000 movies/users/ratings/tags.**

If you want to increase that, you can do so in **ingestion.py**:

```python
N_MOVIES = 1000
N_RATINGS = 1000
N_TAGS = 1000
N_LINKS = 1000
```
 
##### Structure


```
docker
│   README.md
│   docker-compose.yml    
│
└─── ingestion
    │   Dockerfile
    │   ingestion.py
    │   requirements.txt
    │
    └─── data
            links.csv
            movies.csv
            ratings.csv
            tags.csv
```
