-- A procedure to execute when a player is deleted
-- Removes all games that that player played in as well as removes players that
-- no longer have played in a game after the deletion
DELIMITER !
CREATE PROCEDURE delete_player_game(
    p_ign VARCHAR(30),
    p_discrim VARCHAR(5)
)
BEGIN
    DROP TABLE IF EXISTS players_to_del;
    DELETE FROM game WHERE gamehash IN (
        SELECT DISTINCT gamehash FROM game_stat
        WHERE ign = p_ign and discrim = p_discrim
    );

    CREATE TEMPORARY TABLE players_to_del AS
    SELECT ign, discrim FROM player
    WHERE (ign, discrim) NOT IN (SELECT ign, discrim FROM game_stat);

    DELETE FROM player WHERE (ign, discrim) IN (SELECT * FROM players_to_del);
END !
DELIMITER ;

-- Triggers
DELIMITER !                                                                     
                                                                                
-- A procedure to execute when a new game is played
-- Updates the player's statistics with these new statistics if the player
-- exists
-- Adds the player to the view with their first game statistics
-- if the player does not yet exist in the view
CREATE PROCEDURE sp_val_newgame(                                         
    new_ign VARCHAR(30),                                                
    new_discrim VARCHAR(5),
    new_kills   TINYINT,
    new_deaths  TINYINT
)                                                                               
BEGIN                                                                           
    INSERT INTO mv_player_overall_stat 
        -- player not already in view; add row                                  
        VALUES (new_ign, new_discrim, new_kills, new_deaths, 1)
    ON DUPLICATE KEY UPDATE                                                     
        -- player already in view; update existing row                          
        total_kills = total_kills + new_kills,
        total_deaths = total_deaths + new_deaths,
        total_matches = total_matches + 1;
END !                                                                           

-- Handles new rows added to the game_stat table and updates the stats
CREATE TRIGGER trg_game_insert AFTER INSERT ON game_stat FOR EACH ROW
BEGIN
    CALL sp_val_newgame(NEW.ign, NEW.discrim, NEW.kills, NEW.deaths);
END !
DELIMITER ;

-- UDFS
-- Returns the "Page Rank," a statistic we devised heavily weighting
-- first_kills, for the statistics inputted (kills, deaths, assists,
-- first_kills, first_deaths, multi_kills)
DELIMITER !
CREATE FUNCTION page_rank(
    kills TINYINT,
    deaths TINYINT,
    assists TINYINT,
    first_kills TINYINT,
    first_deaths TINYINT,
    multi_kills TINYINT
) RETURNS FLOAT DETERMINISTIC
BEGIN
    RETURN (0.8 * first_kills + 0.3 * kills) * 0.5 - 
           (0.2 * deaths + SQRT(0.3 * first_deaths)) * 0.5 + 0.9 * multi_kills;
END !
DELIMITER ;
