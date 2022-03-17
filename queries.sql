-- Return the map amypham4#7708 has the best ADR in (Equivalent to RA)
WITH 
    avg_map AS (SELECT AVG(adr) AS avg_adr, map 
                FROM game_stat NATURAL JOIN player NATURAL JOIN game
                WHERE ign = 'amypham4' AND discrim = 7708
                GROUP BY map),
    max_map AS (SELECT MAX(avg_adr) AS max_adr FROM avg_map)
SELECT map AS best_adr_map
FROM max_map NATURAL JOIN avg_map
WHERE max_adr = avg_adr;

-- Return the agent that amypham4#7708 has the best ACS with (Equivalent to RA)
WITH 
    avg_agent AS (SELECT AVG(acs) AS avg_acs, agent
                  FROM game_stat NATURAL JOIN player NATURAL JOIN game
                  WHERE ign = 'amypham4' AND discrim = 7708
                  GROUP BY agent),
    max_agent AS (SELECT MAX(avg_acs) AS max_acs FROM avg_agent)
SELECT agent AS best_acs_agent
FROM avg_agent NATURAL JOIN max_agent
WHERE max_acs = avg_acs;

-- Return which players were playing on Friday night
SELECT DISTINCT ign, discrim 
FROM player NATURAL JOIN game_stat NATURAL JOIN game
WHERE DAYOFWEEK(start_time) = 6
ORDER BY ign;

-- Return the total number of wins amypham4#7708 has on each agent 
-- (Equivalent to RA)
SELECT agent, COUNT(gamehash) AS total_wins 
FROM player NATURAL JOIN game_stat NATURAL JOIN game
WHERE ign = 'amypham4' AND discrim = 7708 AND team = 'A'
GROUP BY agent
ORDER BY total_wins DESC;

-- Return which player has the highest average kills in each rank
-- (Equivalent to RA)
WITH 
    rank_stats AS (SELECT ign, discrim, AVG(kills) AS avg_kills, comp_rank
                   FROM player NATURAL JOIN game_stat NATURAL JOIN game
                   GROUP BY ign, discrim, comp_rank),
    max_kills AS (SELECT MAX(avg_kills) AS highest_avg_kills, comp_rank
                  FROM rank_stats 
                  GROUP BY comp_rank)
SELECT ign, discrim, comp_rank, highest_avg_kills 
FROM rank_stats NATURAL JOIN max_kills
WHERE avg_kills = highest_avg_kills
ORDER BY comp_rank;
