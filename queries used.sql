-- -- SQLite
-- -- Movies:
-- -- CREATE TABLE movies ( id INTEGER, title TEXT NOT NULL, year NUMERIC, PRIMARY KEY(id) )

-- -- Rating:
-- -- CREATE TABLE ratings ( movie_id INTEGER NOT NULL, rating REAL NOT NULL, votes INTEGER NOT NULL, FOREIGN KEY(movie_id) REFERENCES movies(id) )

-- -- Stars:
-- -- CREATE TABLE stars ( movie_id INTEGER NOT NULL, person_id INTEGER NOT NULL, FOREIGN KEY(movie_id) REFERENCES movies(id), FOREIGN KEY(person_id) REFERENCES people(id) )

-- -- People:
-- -- CREATE TABLE people ( id INTEGER, name TEXT NOT NULL, birth NUMERIC, PRIMARY KEY(id) )


-- -- 
-- row = db.execute("SELECT * FROM holdings WHERE userId = :userId & symbol = :symb",userId='8', symbol = 'EXPD')

-- SELECT * FROM holdings WHERE symbol =  'EXPD' AND userId = '8'

-- UPDATE holdings SET shares = '2' where userId = '8' AND symbol = 'EXPD'

-- DELETE FROM holdings WHERE userId = '8'

-- DELETE FROM history WHERE userId = '8'

-- UPDATE holdings
-- db.execute("SELECT * FROM users WHERE username = :username",
--                           username=request.form.get("username"))

-- ALTER TABLE holdings DROP COLUMN initPrice

-- -- db.execute("INSERT INTO users (id,username,hash) VALUES (NULL,?,?)",user,h)

-- update users set cash = '10000';

-- drop table holdings;
-- create table holdings(userId INTEGER, symbol TEXT, name TEXT, shares INTEGER, FOREIGN KEY(userId) REFERENCES users(id));

-- drop table history;
-- create table history (userId INTEGER, symbol TEXT, actionType TEXT, shares INTEGER, price DECIMAL(7,2), transDate TEXT, FOREIGN KEY(userId) REFERENCES users(id));


-- select symbol,name,shares from holdings where userId = '8'