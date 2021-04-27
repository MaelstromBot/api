CREATE TABLE IF NOT EXISTS Users (
    id              BIGINT NOT NULL PRIMARY KEY,
    banned          BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Guilds (
    id              BIGINT NOT NULL PRIMARY KEY,
    config          TEXT NOT NULL,
    banned          BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS GuildUsers (
    usr_id          BIGINT NOT NULL REFERENCES Users (id) ON DELETE CASCADE,
    guild_id        BIGINT NOT NULL REFERENCES Guilds (id) ON DELETE CASCADE,
    xp              BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (usr, guild_id)
);

CREATE TABLE IF NOT EXISTS OAuthSessions (
    id              VARCHAR(255) NOT NULL PRIMARY KEY,
    usr_id          BIGINT NOT NULL REFERENCES Users (id) ON DELETE CASCADE,
    expires_at      TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS APIPermissions (
    token           VARCHAR(255) NOT NULL,
    guild_id        BIGINT NOT NULL REFERENCES Guilds (id) ON DELETE CASCADE
);
