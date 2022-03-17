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