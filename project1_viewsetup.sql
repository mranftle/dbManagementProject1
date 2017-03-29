-- SQL Statements
-- Project 1 Database

-- Tables
-- happiness, attack_outcomes, attack_victims, terrorist_attacks


-- Trust and freedom ranking vs attack type -- further query to determine
-- correlation between Trust and Freedom and political attacks
CREATE VIEW attack_targets AS
  SELECT T.country, V.targtype1, COUNT(V.targtype1)
    FROM terrorist_attacks as T, attack_victims as V
      WHERE T.eventid = V.eventid
        GROUP BY T.country, V.targtype1
        ORDER BY T.country;

CREATE VIEW attack_targets_happiness AS
  SELECT A.country, A.targtype1, A.count, H.trust, H.freedom
    FROM attack_targets as A, happiness as H
      WHERE A.country = H.country
      AND A.targtype1 SIMILAR TO '%(Government|Journalists & Media|Police)%';


-- Cumulative number of attacks since 1970
CREATE VIEW cummulative AS
  SELECT T.country, COUNT(T.country) AS attacks
    FROM terrorist_attacks as T
      GROUP BY T.country
      ORDER BY T.country;

-- Cumulative number of attacks since 1970 vs current happiness report
CREATE VIEW cummulative_happiness AS
  SELECT C.country, C.attacks, H.hrank, H.hscore
    FROM cummulative as C, happiness as H
        WHERE C.country = H.country;

-- Number of victims from each country vs country stats in a given year
CREATE VIEW nationalities AS
  SELECT V.natlty1, COUNT(V.natlty1)
    FROM attack_victims as V
      GROUP BY V.natlty1
      ORDER BY V.natlty1;

CREATE VIEW nationalities_happiness AS
  SELECT N.natlty1, N.count, H.hrank, H.hscore
    FROM nationalities as N, happiness as H
      WHERE N.natlty1 = H.country;
