DROP TABLE IF EXISTS match;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS match_stats;
DROP TABLE IF EXISTS team_stats;

CREATE TABLE match(
    gamehash    CHAR(16) PRIMARY KEY,
    map         VARCHAR(10) NOT NULL,
    start_time  DATETIME NOT NULL,
    duration    TIME NOT NULL,
    -- Amount of rounds won by each team
    a_score     TINYINT NOT NULL,
    b_score     TINYINT NOT NULL
);

CREATE TABLE player(
    ign         VARCHAR(30),
    discrim     VARCHAR(4),
    -- Info, if the player is living in Page
    real_name   VARCHAR(30),
    room_num    TINYINT,
    PRIMARY KEY(ign, discrim)
);

CREATE TABLE match_stat(
    gamehash        CHAR(16),
    ign             VARCHAR(30),
    discrim         VARCHAR(4),
    -- Competitive rank
    comp_rank       VARCHAR(20) NOT NULL,
    -- A or B
    team            CHAR(1) NOT NULL,
    agent           VARCHAR(15) NOT NULL,
    -- Average combat score throughout match, rounded
    acs             SMALLINT NOT NULL,
    -- Average damage per round
    adr             NUMERIC(3, 1) NOT NULL,
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
    FOREIGN KEY(gamehash) REFERENCES match(gamehash) ON DELETE CASCADE,
    FOREIGN KEY(ign, discrim) REFERENCES player(ign, discrim) ON DELETE CASCADE,
    INDEX(agent)
);

CREATE TABLE team_stat(
    gamehash    CHAR(16),
    team        CHAR(1),
    -- Average amount team had over all rounds, in their bank/loadout
    bank        SMALLINT NOT NULL,
    loadout     SMALLINT NOT NULL,
    PRIMARY KEY(gamehash, team),
    FOREIGN KEY(gamehash) REFERENCES match(gamehash) ON DELETE CASCADE
);

CREATE INDEX idx_agent ON match_stat(agent);

-- Materialized View for UDFs/Procedures/Triggers
CREATE TABLE mv_player_overall_stat(
    ign             VARCHAR(30),
    discrim         VARCHAR(4),
    total_kills     INT NOT NULL,
    total_deaths    INT NOT NULL,
    total_matches   INT NOT NULL,
    PRIMARY KEY(ign, discrim)
);