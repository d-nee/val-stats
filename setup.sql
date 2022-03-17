DROP TABLE IF EXISTS mv_player_overall_stat;
DROP TABLE IF EXISTS game_stat;
DROP TABLE IF EXISTS team_stat;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS game;

-- Games played and cataloged by the web crawler
-- Includes time, duration, and score information
CREATE TABLE game(
    gamehash    CHAR(36) PRIMARY KEY,
    map         VARCHAR(10) NOT NULL,
    start_time  DATETIME NOT NULL,
    duration    TIME NOT NULL,
    -- Amount of rounds won by each team
    a_score     TINYINT NOT NULL,
    b_score     TINYINT NOT NULL,
    CHECK(a_score >= 0 AND b_score >= 0)
);

-- All players of all games catalogued
-- If the player lives in page house, they have further descriptive data
CREATE TABLE player(
    ign         VARCHAR(30),
    discrim     VARCHAR(5),
    -- Info, if the player is living in Page. Players can have multiple accts.
    real_name   VARCHAR(30) DEFAULT NULL,
    room_num    SMALLINT DEFAULT NULL,
    PRIMARY KEY(ign, discrim)
);

-- Statistics of players who played each game.
-- Includes their rank, team, and a host of statistics.
CREATE TABLE game_stat(
    gamehash        CHAR(36),
    ign             VARCHAR(30),
    discrim         VARCHAR(5),
    -- Competitive rank
    comp_rank       VARCHAR(20) NOT NULL,
    -- A or B, where a team is 'A' if they won
    team            CHAR(1) NOT NULL,
    agent           VARCHAR(15) NOT NULL,
    -- Average combat score throughout match, rounded
    acs             SMALLINT NOT NULL,
    -- Average damage per round
    adr             NUMERIC(5, 2) NOT NULL,
    -- Average econ score throughout match, rounded
    aes             SMALLINT NOT NULL,
    kills           TINYINT NOT NULL,
    deaths          TINYINT NOT NULL,
    assists         TINYINT NOT NULL,
    -- Headshot percentage
    hsp             TINYINT NOT NULL,
    first_kills     TINYINT NOT NULL,
    first_deaths    TINYINT NOT NULL,
    multi_kills     TINYINT NOT NULL,
    PRIMARY KEY(gamehash, ign, discrim),
    FOREIGN KEY(gamehash) REFERENCES game(gamehash) ON DELETE CASCADE,
    FOREIGN KEY(ign, discrim) REFERENCES player(ign, discrim) ON DELETE CASCADE,
    INDEX(agent)
);


-- Team economy statistics, including how much money they saved and spent,
-- on average. Does not include round by round data.
CREATE TABLE team_stat(
    gamehash    CHAR(36),
    team        CHAR(1),
    -- Average amount team had over all rounds, in their bank/loadout
    bank        SMALLINT NOT NULL,
    loadout     SMALLINT NOT NULL,
    PRIMARY KEY(gamehash, team),
    FOREIGN KEY(gamehash) REFERENCES game(gamehash) ON DELETE CASCADE
);


-- Materialized View for UDFs/Procedures/Triggers
-- Contains total kill, death, and game counts for each player.
CREATE TABLE mv_player_overall_stat(
    ign             VARCHAR(30),
    discrim         VARCHAR(5),
    total_kills     INT NOT NULL,
    total_deaths    INT NOT NULL,
    total_matches   INT NOT NULL,
    PRIMARY KEY(ign, discrim)
);
