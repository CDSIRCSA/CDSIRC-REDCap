-- --- SQL to upgrade REDCap to version 12.5.8 from 12.0.2 --- --
USE `redcap`;
SET SESSION SQL_SAFE_UPDATES = 0;

-- SQL for Version 12.0.5 --

REPLACE INTO redcap_config (field_name, value) VALUES
('oauth2_azure_ad_username_attribute', 'userPrincipalName');

-- SQL for Version 12.0.6 --

INSERT INTO redcap_config (field_name, value) VALUES ('fhir_identity_provider', '');

-- SQL for Version 12.0.7 --

set @config_settings_key = (select value from redcap_config where field_name = 'config_settings_key' limit 1);
REPLACE INTO redcap_config (field_name, value) VALUES ('config_settings_key', ifnull(@config_settings_key,''));

-- SQL for Version 12.1.0 --

ALTER TABLE `redcap_surveys` ADD `end_survey_redirect_next_survey_logic` TEXT NULL DEFAULT NULL AFTER `end_survey_redirect_next_survey`;

REPLACE INTO `redcap_validation_types` (`validation_name`, `validation_label`, `regex_js`, `regex_php`, `data_type`, `visible`) 
VALUES ('time_hh_mm_ss', 'Time (HH:MM:SS)', '/^(\d|[01]\d|(2[0-3]))(:[0-5]\d){2}$/', '/^(\d|[01]\d|(2[0-3]))(:[0-5]\d){2}$/', 'time', 1);

-- Drop all FKs for redcap_log_view_requests
ALTER TABLE `redcap_log_view_requests` DROP FOREIGN KEY `redcap_log_view_requests_ibfk_1`;
ALTER TABLE `redcap_log_view_requests` DROP FOREIGN KEY `redcap_log_view_requests_ibfk_2`;

-- Copy the redcap_log_view table
DROP TABLE IF EXISTS redcap_log_view_old;
RENAME TABLE redcap_log_view TO redcap_log_view_old;

CREATE TABLE `redcap_log_view` (
`log_view_id` bigint(19) NOT NULL AUTO_INCREMENT,
`ts` timestamp NULL DEFAULT NULL,
`user` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`event` enum('LOGIN_SUCCESS','LOGIN_FAIL','LOGOUT','PAGE_VIEW') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`ip` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`browser_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`browser_version` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`full_url` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`page` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`project_id` int(10) DEFAULT NULL,
`event_id` int(10) DEFAULT NULL,
`record` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`form_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`miscellaneous` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`session_id` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
PRIMARY KEY (`log_view_id`),
KEY `browser_name` (`browser_name`(191)),
KEY `browser_version` (`browser_version`(191)),
KEY `event` (`event`),
KEY `ip` (`ip`),
KEY `page_ts_project_id` (`page`(191),`ts`,`project_id`),
KEY `project_event_record` (`project_id`,`event_id`,`record`(191)),
KEY `project_record` (`project_id`,`record`(191)),
KEY `session_id` (`session_id`),
KEY `ts_user_event` (`ts`,`user`(191),`event`),
KEY `user_project` (`user`(191),`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Set new auto-increment and backfill 30-minutes of events for temporary continuity purposes
ALTER TABLE redcap_log_view AUTO_INCREMENT = 51539;
insert into redcap_log_view select * from redcap_log_view_old where ts > DATE_SUB(NOW(), INTERVAL 30 MINUTE);

-- Generate system notification from REDCap Messenger
insert into redcap_messages (thread_id, sent_time, message_body) values (1, NOW(), '[{\"title\":\"New feature: Dynamic min\\/max range limits for fields\",\"description\":\"Instead of using exact values as the minimum or maximum range of Textbox fields (e.g., \\\"2021-12-07\\\"), you may now also use \\\"<b>today<\\/b>\\\" and \\\"<b>now<\\/b>\\\" as the min or max so that the current date or time is always used. These can be used to prevent a date\\/time field from having a value in the past or in the future. Additionally, you can now <b>pipe a value from another field<\\/b> into the field\'s min or max range setting - e.g., [visit_date] or [event_1_arm_1][age]. This can help ensure that a Textbox field (whether a date, time, or number) has a larger or smaller value than another field, regardless of whether the field is on the same instrument or not.\\r\\n \\r\\n<b class=\\\"fs15\\\">New action tag: @FORCE-MINMAX<\\/b>\\r\\nThe action tag @FORCE-MINMAX can be used on Textbox fields that have a min or max validation range defined so that no one will not be able to enter a value into the field unless it is within the field\'s specified validation range. This is different from the default behavior in which out-of-range values are permissible. Note: @FORCE-MINMAX is also enforced for data imports to ensure the value is always within the specified range.\",\"link\":\"\",\"action\":\"what-new\"}]');
insert into redcap_messages_status (message_id, recipient_id, recipient_user_id)
select last_insert_id(), '1', ui_id from redcap_user_information where user_suspended_time is null;

-- SQL for Version 12.1.1 --

-- Fix FK issue with redcap_log_view_requests that only affects some installations
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE `redcap_log_view_requests`;
CREATE TABLE `redcap_log_view_requests` (
`lvr_id` bigint(19) NOT NULL AUTO_INCREMENT,
`log_view_id` bigint(19) DEFAULT NULL COMMENT 'FK from redcap_log_view',
`mysql_process_id` int(10) DEFAULT NULL COMMENT 'Process ID for MySQL',
`php_process_id` int(10) DEFAULT NULL COMMENT 'Process ID for PHP',
`script_execution_time` float DEFAULT NULL COMMENT 'Total PHP script execution time (seconds)',
`is_ajax` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Is request an AJAX request?',
`ui_id` int(11) DEFAULT NULL COMMENT 'FK from redcap_user_information',
PRIMARY KEY (`lvr_id`),
UNIQUE KEY `log_view_id` (`log_view_id`),
UNIQUE KEY `log_view_id_time_ui_id` (`log_view_id`,`script_execution_time`,`ui_id`),
KEY `log_view_id_mysql_id_time` (`log_view_id`,`mysql_process_id`,`script_execution_time`),
KEY `mysql_process_id` (`mysql_process_id`),
KEY `php_process_id` (`php_process_id`),
KEY `ui_id` (`ui_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
ALTER TABLE `redcap_log_view_requests`
ADD FOREIGN KEY (`log_view_id`) REFERENCES `redcap_log_view` (`log_view_id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD FOREIGN KEY (`ui_id`) REFERENCES `redcap_user_information` (`ui_id`) ON DELETE SET NULL ON UPDATE CASCADE;
SET FOREIGN_KEY_CHECKS = 1;

-- SQL for Version 12.1.1 --
-- Fix possibly messed up validation type
REPLACE INTO `redcap_validation_types` (`validation_name`, `validation_label`, `regex_js`, `regex_php`, `data_type`, `visible`)
VALUES ('time_hh_mm_ss', 'Time (HH:MM:SS)', '/^(\\d|[01]\\d|(2[0-3]))(:[0-5]\\d){2}$/', '/^(\\d|[01]\\d|(2[0-3]))(:[0-5]\\d){2}$/', 'time', 1);
-- SQL for Version 12.2.0 --

replace into redcap_config (field_name, value) values 
('file_upload_vault_filesystem_authtype', 'AUTH_DIGEST'),
('pdf_econsent_filesystem_authtype', 'AUTH_DIGEST'),
('record_locking_pdf_vault_filesystem_authtype', 'AUTH_DIGEST');

ALTER TABLE `redcap_user_rights` 
    ADD `data_export_instruments` TEXT NULL DEFAULT NULL AFTER `data_export_tool`,
	CHANGE `data_export_tool` `data_export_tool` TINYINT(1) NULL DEFAULT NULL;
ALTER TABLE `redcap_user_roles` 
    ADD `data_export_instruments` TEXT NULL DEFAULT NULL AFTER `data_export_tool`,
	CHANGE `data_export_tool` `data_export_tool` TINYINT(1) NULL DEFAULT NULL;

-- Generate system notification from REDCap Messenger
insert into redcap_messages (thread_id, sent_time, message_body) values (1, NOW(), '[{\"title\":\"New feature: Survey Start Time and new Smart Variables\",\"description\":\"REDCap now collects when participants begin a survey (i.e., the initial time the survey page is opened). Going forward, any responses collected (partial or completed) will have their start time displayed at the top of the data entry form when viewing the response.\\r\\n\\r\\nYou can access the start time via piping by using the new Smart Variables <b>[survey-time-started:instrument]<\\/b> and <b>[survey-date-started:instrument]<\\/b>, which can be used inside the @DEFAULT or @CALCTEXT action tags, among other places. Additionally, you can obtain the total amount of time that has elapsed since the survey was started (in seconds, minutes, etc.) by using <b>[survey-duration:instrument:units]<\\/b> and <b>[survey-duration-completed:instrument:units]<\\/b>. See the Smart Variable documentation for more info.\",\"link\":\"\",\"action\":\"what-new\"}]');
insert into redcap_messages_status (message_id, recipient_id, recipient_user_id)
select last_insert_id(), '1', ui_id from redcap_user_information where user_suspended_time is null;

-- Generate system notification from REDCap Messenger
insert into redcap_messages (thread_id, sent_time, message_body) values (1, NOW(), '[{\"title\":\"Improved data export privileges\",\"description\":\"You may now specify instrument-level privileges regarding a user\'s data export capabilities on the User Rights page in a project. A user may be given \\\"No Access\\\", \\\"De-Identified\\\", \\\"Remove All Identifier Fields\\\", or \\\"Full Data Set\\\" data export rights for EACH data collection instrument. This improvement will make it much easier to match a user\'s Data Exports Rights with their Data Viewing Rights, if you wish, and will give you more granular control regarding what data a user can export from your project.\",\"link\":\"\",\"action\":\"what-new\"}]');
insert into redcap_messages_status (message_id, recipient_id, recipient_user_id)
select last_insert_id(), '1', ui_id from redcap_user_information where user_suspended_time is null;

-- SQL for Version 12.2.1 --
-- Fix possibly messed up password-related config settings
set @password_length = (select value from redcap_config where field_name = 'password_length');
REPLACE INTO redcap_config (field_name, value) VALUES ('password_length', if (@password_length is null, '9', trim(@password_length)));
set @password_complexity = (select value from redcap_config where field_name = 'password_complexity');
REPLACE INTO redcap_config (field_name, value) VALUES ('password_complexity', if (@password_complexity is null, '1', trim(@password_complexity)));
-- SQL for Version 12.2.2 --

-- added column for new survey setting 'pdf_save_translated', default value to 0
ALTER TABLE `redcap_surveys` ADD `pdf_save_translated` TINYINT(1) NOT NULL DEFAULT 0 AFTER `pdf_save_to_event_id`;

-- SQL for Version 12.2.3 --

-- added column for reference value hash, defaults to NULL
ALTER TABLE `redcap_multilanguage_ui` ADD `hash` CHAR(6) COLLATE utf8mb4_unicode_ci DEFAULT NULL AFTER `item`;
ALTER TABLE `redcap_multilanguage_ui_temp` ADD `hash` CHAR(6) COLLATE utf8mb4_unicode_ci DEFAULT NULL AFTER `item`;
-- Add config setting for default form-level full access for new instruments added while in production - value of 0 (default) or 1
set @new_form_default_prod_user_access = (select value from redcap_config where field_name = 'new_form_default_prod_user_access');
REPLACE INTO redcap_config (field_name, value) VALUES ('new_form_default_prod_user_access', if (@new_form_default_prod_user_access is null, '0', trim(@new_form_default_prod_user_access)));
ALTER TABLE `redcap_ehr_fhir_logs` DROP FOREIGN KEY `redcap_ehr_fhir_logs_ibfk_1`;
ALTER TABLE `redcap_ehr_fhir_logs` DROP FOREIGN KEY `redcap_ehr_fhir_logs_ibfk_2`;

ALTER TABLE `redcap_ehr_fhir_logs`
    DROP INDEX project_id_mrn,
    DROP INDEX user_project_mrn_resource,
    DROP `mrn`,
    CHANGE `project_id` `project_id` INT(11) NULL DEFAULT NULL COMMENT 'project ID is NULL during an EHR launch',
    CHANGE `fhir_id` `fhir_id` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
    ADD INDEX project_id_fhir_id  (`project_id`,`fhir_id`),
    ADD INDEX user_project_fhir_id_resource (`user_id`,`project_id`,`fhir_id`,`resource_type`),
    ADD `environment` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'CRON or direct user request' AFTER `status`;
ALTER TABLE `redcap_ehr_fhir_logs`
    ADD FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    ADD FOREIGN KEY (`user_id`) REFERENCES `redcap_user_information` (`ui_id`) ON DELETE CASCADE ON UPDATE CASCADE;

-- SQL for Version 12.2.11 --
replace into redcap_config (field_name, value) values ('amazon_s3_endpoint_url', '');
-- SQL for Version 12.3.0 --

-- Add config settings for OpenID Connect authentication
REPLACE INTO redcap_config (field_name, value) VALUES 
('openid_connect_primary_admin', ''),
('openid_connect_secondary_admin', ''),
('openid_connect_provider_url', ''),
('openid_connect_metadata_url', ''),
('openid_connect_client_id', ''),
('openid_connect_client_secret', '');

ALTER TABLE `redcap_surveys` 
    ADD `survey_width_percent` INT(3) NULL DEFAULT NULL,
    ADD `survey_show_font_resize` tinyint(1) NOT NULL DEFAULT '1',
    ADD `survey_btn_text_prev_page` text NULL DEFAULT NULL,
    ADD `survey_btn_text_next_page` text NULL DEFAULT NULL,
    ADD `survey_btn_text_submit` text NULL DEFAULT NULL,
    ADD `survey_btn_hide_submit` tinyint(1) NOT NULL DEFAULT '0',
    ADD `survey_btn_hide_submit_logic` text NULL DEFAULT NULL;

-- New setting to enable Database Query Tool
set @database_query_tool_enabled = (select value from redcap_config where field_name = 'database_query_tool_enabled');
REPLACE INTO redcap_config (field_name, value) VALUES ('database_query_tool_enabled', if (@database_query_tool_enabled is null, '0', trim(@database_query_tool_enabled)));
-- New table for Database Query Tool
CREATE TABLE IF NOT EXISTS `redcap_custom_queries` (
`qid` int(10) NOT NULL AUTO_INCREMENT,
`title` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`query` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
PRIMARY KEY (`qid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Disable the MySQL Simple Admin EM
DELETE s.* FROM redcap_external_modules e, redcap_external_module_settings s
    WHERE e.directory_prefix = 'mysql_simple_admin' AND e.external_module_id = s.external_module_id AND s.project_id IS NULL AND s.`key` = 'version';

-- SQL for Version 12.3.1 --

-- Add config setting to disable the e-signature feature
REPLACE INTO redcap_config (field_name, value) VALUES ('esignature_enabled_global', '1');

-- SQL for Version 12.3.2 --

-- Enable the REDCap URL Shortener
UPDATE redcap_config SET value = '1' WHERE field_name = 'enable_url_shortener_redcap';

CREATE TABLE `redcap_crons_datediff` (
`dd_id` int(10) NOT NULL AUTO_INCREMENT,
`project_id` int(10) DEFAULT NULL,
`record` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`asi_updated_at` datetime DEFAULT NULL COMMENT 'Last evaluation for ASIs',
`asi_status` enum('QUEUED','PROCESSING') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Status for ASIs',
`alert_updated_at` datetime DEFAULT NULL COMMENT 'Last evaluation for Alerts',
`alert_status` enum('QUEUED','PROCESSING') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Status for Alerts',
PRIMARY KEY (`dd_id`),
UNIQUE KEY `project_record` (`project_id`,`record`),
KEY `alert_status_updated_at` (`alert_status`,`alert_updated_at`),
KEY `alert_updated_at` (`alert_updated_at`),
KEY `asi_status_updated_at` (`asi_status`,`asi_updated_at`),
KEY `asi_updated_at` (`asi_updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE `redcap_crons_datediff`
ADD FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE;

INSERT INTO redcap_crons (cron_name, cron_description, cron_enabled, cron_frequency, cron_max_run_time, cron_instances_max, cron_instances_current, cron_last_run_end, cron_times_failed, cron_external_url) VALUES
('QueueRecordsDatediffCheckerCrons', 'Queue records that are ready to be evaluated by the datediff cron jobs.', 'ENABLED', 600, 1800, 1, 0, NULL, 0, NULL),
('AlertsNotificationsDatediffChecker2', 'Process records that are already queued for the Alerts datediff cron job.', 'ENABLED', 60, 3600, 5, 0, NULL, 0, NULL),
('AutomatedSurveyInvitationsDatediffChecker3', 'Process records that are already queued for the ASI datediff cron job.', 'ENABLED', 60, 3600, 5, 0, NULL, 0, NULL);

-- SQL for Version 12.3.2 --
INSERT INTO `redcap_validation_types` (`validation_name`, `validation_label`, `regex_js`, `regex_php`, `data_type`, `legacy_value`, `visible`)
VALUES ('phone_uk', 'Phone (UK)', '/^((((\\+44|0044)\\s?\\d{4}|\\(?0\\d{4}\\)?)\\s?\\d{3}\\s?\\d{3})|(((\\+44|0044)\\s?\\d{3}|\\(?0\\d{3}\\)?)\\s?\\d{3}\\s?\\d{4})|(((\\+44|0044)\\s?\\d{2}|\\(?0\\d{2}\\)?)\\s?\\d{4}\\s?\\d{4}))(\\s?\\#(\\d{4}|\\d{3}))?$/', '/^((((\\+44|0044)\\s?\\d{4}|\\(?0\\d{4}\\)?)\\s?\\d{3}\\s?\\d{3})|(((\\+44|0044)\\s?\\d{3}|\\(?0\\d{3}\\)?)\\s?\\d{3}\\s?\\d{4})|(((\\+44|0044)\\s?\\d{2}|\\(?0\\d{2}\\)?)\\s?\\d{4}\\s?\\d{4}))(\\s?\\#(\\d{4}|\\d{3}))?$/', 'phone', NULL, 0);
-- SQL for Version 12.3.3 --

REPLACE INTO redcap_config (field_name, value) VALUES ('two_factor_auth_esign_pin', '0');

-- SQL for Version 12.4.0 --

-- Add config setting to disable the calendar feed feature
REPLACE INTO redcap_config (field_name, value) VALUES ('calendar_feed_enabled_global', '1');

-- Adding calendar feed hash to project
CREATE TABLE `redcap_events_calendar_feed` (
`feed_id` int(10) NOT NULL AUTO_INCREMENT,
`project_id` int(10) DEFAULT NULL,
`record` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`userid` int(11) DEFAULT NULL COMMENT 'NULL=survey participant',
`hash` varchar(100) CHARACTER SET latin1 COLLATE latin1_general_cs DEFAULT NULL,
PRIMARY KEY (`feed_id`),
UNIQUE KEY `hash` (`hash`),
UNIQUE KEY `project_record_user` (`project_id`,`record`,`userid`),
KEY `project_userid` (`project_id`,`userid`),
KEY `userid` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
ALTER TABLE `redcap_events_calendar_feed`
ADD FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD FOREIGN KEY (`userid`) REFERENCES `redcap_user_information` (`ui_id`) ON DELETE CASCADE ON UPDATE CASCADE;

REPLACE INTO redcap_config (field_name, value) VALUES
('oauth2_azure_ad_endpoint_version', 'V1');

ALTER TABLE `redcap_outgoing_email_sms_log` 
    CHANGE `type` `type` ENUM('EMAIL','SMS','VOICE_CALL','SENDGRID_TEMPLATE') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'EMAIL';

alter table redcap_projects 
    add sendgrid_enabled TINYINT(1) NOT NULL DEFAULT '0',
    add sendgrid_project_api_key TEXT NULL DEFAULT NULL;

alter table redcap_alerts 
    add sendgrid_template_id TEXT NULL DEFAULT NULL,
    add sendgrid_template_data TEXT NULL DEFAULT NULL;

ALTER TABLE `redcap_alerts` 
    CHANGE `alert_type` `alert_type` ENUM('EMAIL','SMS','VOICE_CALL','SENDGRID_TEMPLATE') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'EMAIL';

ALTER TABLE `redcap_alerts_sent_log` 
    CHANGE `alert_type` `alert_type` ENUM('EMAIL','SMS','VOICE_CALL','SENDGRID_TEMPLATE') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'EMAIL';

REPLACE INTO redcap_config (field_name, value) VALUES ('sendgrid_enabled_global', 1);
REPLACE INTO redcap_config (field_name, value) VALUES ('sendgrid_enabled_by_super_users_only', 0);
REPLACE INTO redcap_config (field_name, value) VALUES ('sendgrid_display_info_project_setup', 0);

update redcap_crons set cron_enabled = 'DISABLED' where cron_name in ('AutomatedSurveyInvitationsDatediffChecker2', 'AlertsNotificationsDatediffChecker');

REPLACE INTO redcap_config (field_name, value) VALUES ('openid_connect_name', '');
REPLACE INTO redcap_config (field_name, value) VALUES ('openid_connect_username_attribute', 'username');

ALTER TABLE `redcap_crons_datediff` 
    ADD `asi_last_update_start` DATETIME NULL DEFAULT NULL AFTER `asi_updated_at`, 
    ADD `alert_last_update_start` DATETIME NULL DEFAULT NULL AFTER `alert_updated_at`, 
    ADD INDEX `asi_last_update_status` (`asi_last_update_start`, `asi_status`),
    ADD INDEX `alert_last_update_status` (`alert_last_update_start`, `alert_status`);

-- SQL for Version 12.4.1 --

-- Add config setting for 2FA
REPLACE INTO redcap_config (field_name, value) VALUES ('two_factor_auth_enforce_table_users_only', '0');

-- SQL for Version 12.4.2 --

delete from redcap_external_module_settings where project_id is not null and project_id not in (select project_id from redcap_projects);

-- SQL for Version 12.4.4 --

ALTER TABLE `redcap_ehr_fhir_logs` 
    ADD `mrn` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '', 
    ADD INDEX `mrn` (`mrn`),
    ADD INDEX `project_id_mrn` (`project_id`, `mrn`),
    ADD INDEX `fhir_id_resource_type` (`fhir_id`, `resource_type`);

-- SQL for Version 12.5.0 --

DELETE FROM `redcap_surveys_scheduler` WHERE instance = 'AFTER_FIRST';
ALTER TABLE `redcap_surveys_scheduler`
    ADD `num_recurrence` INT(5) NOT NULL DEFAULT '0' AFTER `instance`,
    ADD `units_recurrence` enum('DAYS','HOURS','MINUTES') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'DAYS' AFTER `num_recurrence`,
    ADD `max_recurrence` INT(5) NULL DEFAULT NULL AFTER `units_recurrence`,
    DROP INDEX `survey_event_instance`, 
    ADD UNIQUE `survey_event` (`survey_id`, `event_id`);

CREATE TABLE `redcap_surveys_scheduler_recurrence` (
`ssr_id` int(10) NOT NULL AUTO_INCREMENT,
`ss_id` int(10) DEFAULT NULL,
`creation_date` datetime DEFAULT NULL,
`record` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`event_id` int(10) DEFAULT NULL,
`instrument` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`times_sent` smallint(4) DEFAULT NULL,
`last_sent` datetime DEFAULT NULL,
`status` enum('IDLE','QUEUED','SENDING') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'IDLE',
`first_send_time` datetime DEFAULT NULL,
`next_send_time` datetime DEFAULT NULL,
PRIMARY KEY (`ssr_id`),
UNIQUE KEY `ss_id_record_event_instrument` (`ss_id`,`record`,`event_id`,`instrument`),
KEY `creation_date` (`creation_date`),
KEY `event_record` (`event_id`,`record`),
KEY `first_send_time` (`first_send_time`),
KEY `last_sent` (`last_sent`),
KEY `next_send_time_status_ss_id` (`next_send_time`,`status`,`ss_id`),
KEY `ss_id_status_times_sent` (`status`,`ss_id`,`times_sent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE `redcap_surveys_scheduler_recurrence`
ADD FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD FOREIGN KEY (`ss_id`) REFERENCES `redcap_surveys_scheduler` (`ss_id`) ON DELETE CASCADE ON UPDATE CASCADE;

-- Generate system notification from REDCap Messenger
insert into redcap_messages (thread_id, sent_time, message_body) values (1, NOW(), '[{\"title\":\"New feature: Repeating ASIs\",\"description\":\"You can now set Automated Survey Invitations (ASIs) to send multiple times on a recurring basis for any given survey in your project. If the survey is a repeating instrument or if it exists on a repeating event, you will see a new section \\\"How many times to send it\\\" in the ASI setup popup in the Online Designer. There you may set the ASI to send survey invitations repeatedly at a regular interval, in which it can repeat forever or a set number of times. The new repeating ASI feature works similarly to recurring alerts for Alerts & Notifications.\\r\\n\\r\\n<b class=\\\"fs15\\\">New Smart Variable: [new-instance]<\\/b>\\r\\nThis new Smart Variable can be appended to [survey-link] or [form-link] to create a link to a new, not-yet-created repeating instance for the current record. For example, you can create a recurring alert that contains <code>[survey-url:repeating_survey][new-instance]<\\/code> in the text, in which it will send the recipient a survey link for creating a new instance of a repeating survey.\\r\\n\\r\\n<b class=\\\"fs15\\\">Embedding images in text & emails<\\/b>\\r\\nYou may now embed an inline image into the text of a survey invitation, an alert, or a field label on a form\\/survey by clicking the <i class=\\\"far fa-image\\\"><\\/i> icon in the rich text editor, and then uploading an image from your local device. Anywhere that the rich text editor is used, you may embed an image into its text (with one exception: the @RICHTEXT action tag on public surveys).\",\"link\":\"\",\"action\":\"what-new\"}]');
insert into redcap_messages_status (message_id, recipient_id, recipient_user_id)
select last_insert_id(), '1', ui_id from redcap_user_information where user_suspended_time is null;

-- SQL for Version 12.5.0 --
REPLACE INTO redcap_config (field_name, value) VALUES
('rich_text_image_embed_enabled', '1');
-- SQL for Version 12.5.3 --
update redcap_surveys set text_to_speech = 0, text_to_speech_language = 'en-US_AllisonV3Voice'
    where text_to_speech_language = 'ar-AR_OmarVoice';
-- SQL for Version 12.5.5 --
REPLACE INTO redcap_config (field_name, value) VALUES
('contact_admin_button_url', '');
-- SQL for Version 12.5.6 --

ALTER TABLE `redcap_alerts` ADD `sendgrid_mail_send_configuration` TEXT NULL DEFAULT NULL AFTER `sendgrid_template_data`;


-- Set date of upgrade --
UPDATE redcap_config SET value = CURDATE() WHERE field_name = 'redcap_last_install_date';
REPLACE INTO redcap_history_version (`date`, redcap_version) values (CURDATE(), '12.5.8');
-- Set new version number --
UPDATE redcap_config SET value = '12.5.8' WHERE field_name = 'redcap_version';
