CREATE DATABASE IF NOT EXISTS demo;
USE demo;
CREATE TABLE IF NOT EXISTS sensors (
  ts TIMESTAMP,
  temperature FLOAT,
  humidity FLOAT
) TAGS (device_id BINARY(20));

INSERT INTO sensors USING demo.sensors TAGS ('device001') VALUES (NOW, 27.1, 19.0);

SELECT * FROM sensors WHERE ts > NOW - 1h;
