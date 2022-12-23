CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name varchar(255),
    created_at timestamp
);

CREATE TABLE url_checks (
    id bigint PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    url_id bigint REFERENCES urls (id),
    status_code bigint,
    h1 varchar(255),
    title varchar(255),
    description varchar(255),
    created_at timestamp
);
INSERT INTO url_checks (url_id, status_code, created_at) VALUES (49, 200, '2022-12-17 19:23:10.922933');
TRUNCATE TABLE urls RESTART IDENTITY CASCADE;
TRUNCATE TABLE url_checks;