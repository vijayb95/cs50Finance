-- SQLite
-- Movies:
-- CREATE TABLE movies ( id INTEGER, title TEXT NOT NULL, year NUMERIC, PRIMARY KEY(id) )

-- Rating:
-- CREATE TABLE ratings ( movie_id INTEGER NOT NULL, rating REAL NOT NULL, votes INTEGER NOT NULL, FOREIGN KEY(movie_id) REFERENCES movies(id) )

-- Stars:
-- CREATE TABLE stars ( movie_id INTEGER NOT NULL, person_id INTEGER NOT NULL, FOREIGN KEY(movie_id) REFERENCES movies(id), FOREIGN KEY(person_id) REFERENCES people(id) )

-- People:
-- CREATE TABLE people ( id INTEGER, name TEXT NOT NULL, birth NUMERIC, PRIMARY KEY(id) )


-- create table holdings(userId INTEGER, symbol TEXT, name TEXT, shares INTEGER, FOREIGN KEY(userId) REFERENCES users(id))


-- db.execute("INSERT INTO users (id,username,hash) VALUES (NULL,?,?)",user,h)


create table history (userId INTEGER, symbol TEXT, actionType TEXT, shares INTEGER, price INTEGER, transDate TEXT, FOREIGN KEY(userId) REFERENCES users(id))