SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";
SET SQL_MODE='ALLOW_INVALID_DATES';

CREATE DATABASE IF NOT EXISTS `epytodo` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;
USE `epytodo`;

CREATE TABLE IF NOT EXISTS `task` (
  `task_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `begin` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `end` TIMESTAMP NULL DEFAULT NULL,
  `status` enum('not started','in progress','done') NOT NULL DEFAULT 'not started',
  PRIMARY KEY (`task_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `user_has_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_user_id` int(11) NOT NULL,
  `fk_task_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_id` (`fk_user_id`),
  KEY `fk_task_id` (`fk_task_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


ALTER TABLE `user_has_task`
  ADD CONSTRAINT `fk_task_id` FOREIGN KEY (`fk_task_id`) REFERENCES `task` (`task_id`),
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`fk_user_id`) REFERENCES `user` (`user_id`);
COMMIT;
