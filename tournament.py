#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    pg=connect()
    c=pg.cursor()
    c.execute("delete from match")
    pg.commit()
    pg.close()

def deletePlayers():
    """Remove all the player records from the database."""
    pg=connect()
    c=pg.cursor()
    c.execute("delete from player")
    deleteMatches()
    pg.commit()
    pg.close()

def countPlayers():
    """Returns the number of players currently registered."""
    pg=connect()
    c=pg.cursor()
    c.execute("select count(*) from player")
    rows=c.fetchall()
    pg.close()
    return rows[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    pg=connect()
    c=pg.cursor()
    c.execute("insert into player (name) values(%s)",(name,))
    pg.commit()
    pg.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    pg=connect()
    c=pg.cursor()
    c.execute("select player.id as id, player.name as name, count(match.winner_id) as num from player left join match on player.id=match.winner_id group by player.id order by num")
    rows=c.fetchall()
    new_rows=[]
    for i in rows:
	i=list(i)
	c.execute("select * from match where winner_id=(%s) or loser_id=(%s)",(i[0],i[0],))
        #print i[0]
	#print "select * from match where winner_id=(%s) or loser_id=(%s)"%(i[0],i[0],)
        row=c.fetchall()
        #print row
	i.append(len(row))
	new_rows.append(i)
    pg.close()
    return new_rows;

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    pg=connect()
    c=pg.cursor()
    c.execute("insert into match (winner_id,loser_id,winner) values(%s,%s,%s)",(winner,loser,winner,))
    pg.commit()
    pg.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    data=playerStandings()
    length=len(data)
    res=[]
    for i in range(length/2):
	  temp=(data[2*i][0],data[2*i][1],data[2*i+1][0],data[2*i+1][1])
          res.append(temp)
    return res
