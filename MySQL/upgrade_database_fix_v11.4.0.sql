-- SQL TO REPAIR REDCAP TABLES
USE `redcap`;
SET SESSION SQL_SAFE_UPDATES = 0;
SET FOREIGN_KEY_CHECKS = 0;
ALTER TABLE `redcap_user_roles` ADD KEY (`project_id`);
ALTER TABLE `redcap_new_record_cache` ADD FOREIGN KEY (`arm_id`) REFERENCES `redcap_events_arms` (`arm_id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `redcap_new_record_cache` ADD FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `redcap_new_record_cache` ADD FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `redcap_outgoing_email_sms_identifiers` ADD FOREIGN KEY (`ssq_id`) REFERENCES `redcap_surveys_scheduler_queue` (`ssq_id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `redcap_outgoing_email_sms_log` ADD FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE `redcap_outgoing_email_sms_log` ADD FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`);
SET FOREIGN_KEY_CHECKS = 1;
