#!/usr/bin/bash

PASSWORD=$IG_PASSWD
if test -f "$IG_PASSWD_FILE"; then
    PASSWORD=$(head -n 1 $IG_PASSWD_FILE)
    PASSWORD=${PASSWORD%$'\n'}
fi

psql "postgresql://${IG_USER}:${PASSWORD}@${PG_HOST}:${PG_PORT}/${IG_DATABASE}" <<-EOSQL
create table if not exists users ( username varchar(100) NOT NULL PRIMARY KEY, password varchar(100), full_name varchar(200));
create table if not exists images (id SERIAL PRIMARY KEY,username VARCHAR(100) NOT NULL, filename VARCHAR(500) NOT NULL);
insert into users values ('dongji', 'cpsc4973', 'dongji') on conflict (username) do nothing;
 GRANT ALL PRIVILEGES ON TABLE users TO ${IG_USER};
 GRANT ALL PRIVILEGES ON TABLE images TO ${IG_USER};
EOSQL
