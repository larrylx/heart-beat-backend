CREATE TABLE `user_basic` (
  `user_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'User ID',
  `user_name` varchar(32) NOT NULL COMMENT 'User Name',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'User Status, 0-Disable，1-Normal',
  `click_time` tinyint(24) NOT NULL DEFAULT '8' COMMENT 'Hours Need to Re click',
  `remind_email` varchar(320) NOT NULL COMMENT 'User Reminder Email',
  `alert_email` varchar(640) NOT NULL COMMENT 'User Alert Email',
  `profile_photo` varchar(128) NULL COMMENT 'Profile Picture',
  `last_login` datetime NULL COMMENT 'User Last Log in Time',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='User Info Table';