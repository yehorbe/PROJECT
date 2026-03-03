create database when_pigs_fly;
use when_pigs_fly;  
SOURCE C:/Users/yehor/Downloads/flight_simulator_database_script.sql
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS goal;
DROP TABLE IF EXISTS goal_reached;
DROP TABLE IF EXISTS airport;


CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(40) NULL,
    origin VARCHAR(40),
    CONSTRAINT fk_origin 
        FOREIGN KEY (origin) 
        REFERENCES country(iso_country)
)CHARSET=latin1;


CREATE TABLE game (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(40) NULL,
    role VARCHAR(40),
	money int,
	location VARCHAR(40),
    CONSTRAINT fk_location
        FOREIGN KEY (location) 
        REFERENCES country(iso_country)
)CHARSET=latin1;

CREATE TABLE player_inventory (
    game_id INT NOT NULL,
    item_id INT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);

CREATE TABLE goal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(40),
    decription VARCHAR(200),
	salary_goal INT,
    salary_text VARCHAR(40),
	target VARCHAR(40)
)CHARSET=latin1;

insert into goal (name, decription, salary_goal, salary_text, target)
values  ('EARN', 'The amount player have to earn by selling items in different countries', 5000, 'The max value', 'Euros'),
('Steal', 'The amount thieve have to steal by taking items from other players and selling in different countries', 1000, 'The max value', 'Euros'),
('Catch', 'Police have to catch thieves', 0, 'NO max or min value', 'Catch thieves');

insert into items (origin, name)
values ('AD', 'cigar'),
('AL', 'handmade carpets'),
('AT', 'mozartkugel'),
('BA', 'copper coffee set'),
('BE', 'handmade chocolate'),
('BG', 'Rose essential oil'),
('BY', 'linen clothing'),
('CH', 'high-end watches'),
('CZ', 'czech crystal'),e4
('DE', 'dark beer'),
('DK', 'royal porcelain'),
('EE', 'amber jewelry'),
('ES', 'Iberian ham'),
('FI', 'Moomin doll'),
('FO', 'dried fish'),
('FR', 'High-end skincare products'),
('GB', 'Bone China Tea Set'),
('GG', 'abalone'),
('GI', 'olive oil'),
('GR', 'handmade leather sandals'),
('HR', 'red coral jewelry'),
('HU', 'Fruit Brandy'),
('IE', 'Irish whiskey'),
('IM', 'Queen Scallop'),
('IS', 'handmade candles'),
('IT', 'handmade leather bags'),
('JE', 'black butter'),
('LI', 'commemorative stamps'),
('LT', 'Wood carving'),
('LU', 'grape wine'),
('LV', 'black balsam'),
('MC', 'monaco essential oil'),
('MD', 'golden millet'),
('ME', 'truffle sauce'),
('MK', 'Hand-painted porcelain tiles'),
('MT', 'malta knights statue'),
('NL', 'wooden shoes'),
('NO', 'deep-sea fish oil'),
('PL', 'kabanos'),
('PT', 'royal Soap'),
('RO', 'pipe'),
('RS', 'honey'),
('SE', 'handmade silver jewelry'),
('SI', 'Idrija Lace'),
('SK', 'herbal bitter wine'),
('SM', 'cheese'),
('UA', 'cherry liqueur'),
('VA', 'holy grail'),

('XK', 'stringed instrument');
