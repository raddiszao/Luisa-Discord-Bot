/*
Navicat MySQL Data Transfer

Source Server         : luisa
Source Server Version : 80022
Source Host           : 192.95.52.247:3306
Source Database       : luisarpg

Target Server Type    : MYSQL
Target Server Version : 80022
File Encoding         : 65001

Date: 2020-12-16 22:22:15
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for messages
-- ----------------------------
DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_from_id` varchar(255) DEFAULT NULL,
  `user_to_id` varchar(255) DEFAULT NULL,
  `message` varchar(900) DEFAULT NULL,
  `timestamp` int DEFAULT NULL,
  `read` enum('1','0') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` varchar(255) NOT NULL,
  `guild_id` varchar(255) NOT NULL DEFAULT '0',
  `xp_points` int DEFAULT '0',
  `xp_deposited` int DEFAULT '0',
  `deaths` int DEFAULT '0',
  `kills` int DEFAULT '0',
  `married_id` varchar(255) DEFAULT '',
  `stuck` enum('0','1') DEFAULT '0',
  `arrested` int DEFAULT '0',
  `daily_time` int DEFAULT '0',
  `job_time` int DEFAULT '0',
  `bet_time` int DEFAULT '0',
  `assault_time` int DEFAULT '0',
  `week_time` int DEFAULT '0',
  `month_time` int DEFAULT '0',
  `shoot_time` int DEFAULT '0',
  `hacker_time` int DEFAULT '0',
  `kill_time` int DEFAULT '0',
  `stuck_time` int DEFAULT '0',
  `punch_time` int DEFAULT '0',
  `coinflip_time` int DEFAULT '0',
  `wanted` enum('0','1') DEFAULT '0',
  `hunger` int DEFAULT '100',
  `items` varchar(5000) DEFAULT '',
  `bullets` int DEFAULT '0',
  `level` int DEFAULT '1',
  `progress_level` int DEFAULT '0',
  `health` int DEFAULT '100',
  `westcoast` int DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
