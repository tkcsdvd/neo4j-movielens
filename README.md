# Load MovieLens Dataset Into Neo4j

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