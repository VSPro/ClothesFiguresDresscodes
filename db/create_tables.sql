BEGIN;

\c workshop

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 36ab5b8b26a0

CREATE TABLE users (
    id BIGSERIAL NOT NULL, 
    email VARCHAR(255) NOT NULL, 
    email_confirmed_at TIMESTAMP WITHOUT TIME ZONE, 
    username VARCHAR(50) NOT NULL, 
    _password BYTEA NOT NULL, 
    country VARCHAR(128), 
    company VARCHAR(128), 
    uuid VARCHAR(64) NOT NULL, 
    password_changed_at TIMESTAMP WITHOUT TIME ZONE, 
    active BOOLEAN, 
    first_name VARCHAR(50), 
    last_name VARCHAR(50), 
    PRIMARY KEY (id), 
    UNIQUE (email), 
    UNIQUE (username), 
    UNIQUE (uuid)
);

CREATE TABLE api_key (
    id BIGSERIAL NOT NULL, 
    user_id BIGINT NOT NULL, 
    usage_plan_id VARCHAR(256), 
    api_key_id VARCHAR(256), 
    plan_key_id VARCHAR(256), 
    api_key VARCHAR(256), 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    active BOOLEAN, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE passphrase (
    id BIGSERIAL NOT NULL, 
    user_id BIGINT NOT NULL, 
    question VARCHAR(256), 
    answer VARCHAR(256), 
    active BOOLEAN, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

INSERT INTO alembic_version (version_num) VALUES ('36ab5b8b26a0');

COMMIT;