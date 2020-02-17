CREATE TABLE games (
  id int(11) NOT NULL AUTO_INCREMENT,
  winner varchar(10) NOT NULL,
  total_size int(15) NOT NULL,
  board_config varchar(2000),
  black_player varchar(20),
  white_player varchar(20),
  created_time datetime NOT NULL,

  PRIMARY KEY (id),
  KEY idx_winner (winner)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE game_logs (
  id int(11) NOT NULL AUTO_INCREMENT,
  game_id int(11) NOT NULL,
  idx int(15) NOT NULL,
  total_size int(15) NOT NULL,
  stone_color varchar(20),
  x_axis int(15),
  y_axis int(25),

  PRIMARY KEY (id),
  KEY idx_game_id (game_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;