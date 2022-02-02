CREATE TABLE `click_log` (
  `click_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Click ID',
  `user_id` bigint(20) NOT NULL COMMENT 'User ID',
  `click_time` datetime NOT NULL COMMENT 'Check-In Time',
  PRIMARY KEY (`click_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Every Click Record';