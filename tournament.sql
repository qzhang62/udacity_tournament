-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table player(id serial primary key, name text);
create table match(math_id serial primary key,winner_id serial references player(id), loser_id serial references player(id),winner serial references player(id));
