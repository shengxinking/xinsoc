/*
Navicat MySQL Data Transfer

Source Server         : 192.168.138.102
Source Server Version : 50537
Source Host           : 192.168.138.102:3306
Source Database       : port_scan

Target Server Type    : MYSQL
Target Server Version : 50537
File Encoding         : 65001

Date: 2015-07-07 13:47:35
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `config`
-- ----------------------------
DROP TABLE IF EXISTS `config`;
CREATE TABLE `config` (
  `ip` char(255) COLLATE utf8_bin NOT NULL DEFAULT '',
  `relate_man` char(255) COLLATE utf8_bin DEFAULT NULL,
  `service` char(255) COLLATE utf8_bin DEFAULT NULL,
  `mail` char(255) COLLATE utf8_bin DEFAULT NULL,
  `phone` char(255) COLLATE utf8_bin DEFAULT NULL,
  `region` char(255) COLLATE utf8_bin DEFAULT NULL,
  `scan_port` char(255) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of config
-- ----------------------------
INSERT INTO `config` VALUES ('192.168.138.39', null, null, null, null, null, 'U:53,111,137,T:21-25,80,139,8080');

-- ----------------------------
-- Table structure for `result`
-- ----------------------------
DROP TABLE IF EXISTS `result`;
CREATE TABLE `result` (
  `ip` char(255) COLLATE utf8_bin NOT NULL DEFAULT '',
  `relate_man` char(255) COLLATE utf8_bin DEFAULT NULL,
  `port` char(255) COLLATE utf8_bin DEFAULT NULL,
  `service` char(255) COLLATE utf8_bin DEFAULT NULL,
  `mail` char(255) COLLATE utf8_bin DEFAULT NULL,
  `phone` char(255) COLLATE utf8_bin DEFAULT NULL,
  `region` char(255) COLLATE utf8_bin DEFAULT NULL,
  `state` char(255) COLLATE utf8_bin DEFAULT NULL,
  `banner` char(255) COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of result
-- ----------------------------
INSERT INTO `result` VALUES ('192.168.138.39', '', '21', 'ftp', '', '', '', 'open', 'product: FileZilla ftpd version: 0.9.45 beta ostype: Windows');
