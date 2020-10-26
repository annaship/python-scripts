# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.5.5-10.4.11-MariaDB)
# Database: mcm_history
# Generation Time: 2020-10-26 15:44:41 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table bibliographic_citation
# ------------------------------------------------------------

DROP TABLE IF EXISTS `bibliographic_citation`;

CREATE TABLE `bibliographic_citation` (
  `bibliographic_citation_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `bibliographic_citation` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`bibliographic_citation_id`),
  UNIQUE KEY `bibliographic_citation` (`bibliographic_citation`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table content
# ------------------------------------------------------------

DROP TABLE IF EXISTS `content`;

CREATE TABLE `content` (
  `content_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `content` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`content_id`),
  UNIQUE KEY `content` (`content`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table content_url
# ------------------------------------------------------------

DROP TABLE IF EXISTS `content_url`;

CREATE TABLE `content_url` (
  `content_url_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `content_url` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`content_url_id`),
  UNIQUE KEY `content_url` (`content_url`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table coverage_lat
# ------------------------------------------------------------

DROP TABLE IF EXISTS `coverage_lat`;

CREATE TABLE `coverage_lat` (
  `coverage_lat_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `coverage_lat` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`coverage_lat_id`),
  UNIQUE KEY `coverage_lat` (`coverage_lat`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table coverage_long
# ------------------------------------------------------------

DROP TABLE IF EXISTS `coverage_long`;

CREATE TABLE `coverage_long` (
  `coverage_long_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `coverage_long` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`coverage_long_id`),
  UNIQUE KEY `coverage_long` (`coverage_long`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table description
# ------------------------------------------------------------

DROP TABLE IF EXISTS `description`;

CREATE TABLE `description` (
  `description_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `description` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`description_id`),
  UNIQUE KEY `description` (`description`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table digitization_specifications
# ------------------------------------------------------------

DROP TABLE IF EXISTS `digitization_specifications`;

CREATE TABLE `digitization_specifications` (
  `digitization_specifications_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `digitization_specifications` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`digitization_specifications_id`),
  UNIQUE KEY `digitization_specifications` (`digitization_specifications`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table entry
# ------------------------------------------------------------

DROP TABLE IF EXISTS `entry`;

CREATE TABLE `entry` (
  `entry_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `bibliographic_citation_id` int(11) unsigned NOT NULL,
  `content_id` int(11) unsigned NOT NULL,
  `content_url_id` int(11) unsigned NOT NULL,
  `content_url_audio_id` int(11) unsigned NOT NULL,
  `content_url_transcript_id` int(11) unsigned NOT NULL,
  `contributor_id` int(11) unsigned NOT NULL,
  `country_id` int(11) unsigned NOT NULL,
  `coverage_lat_id` int(11) unsigned NOT NULL,
  `coverage_long_id` int(11) unsigned NOT NULL,
  `creator_id` int(11) unsigned NOT NULL,
  `creator_other_id` int(11) unsigned NOT NULL,
  `date_digital_id` int(11) unsigned NOT NULL,
  `date_exact_id` int(11) unsigned NOT NULL,
  `date_season_id` int(11) unsigned NOT NULL,
  `date_season_yyyy_id` int(11) unsigned NOT NULL,
  `description_id` int(11) unsigned NOT NULL,
  `digitization_specifications_id` int(11) unsigned NOT NULL,
  `format_id` int(11) unsigned NOT NULL,
  `identifier_id` int(11) unsigned NOT NULL,
  `language_id` int(11) unsigned NOT NULL,
  `publisher_id` int(11) unsigned NOT NULL,
  `publisher_location_id` int(11) unsigned NOT NULL,
  `relation_id` int(11) unsigned NOT NULL,
  `rights_id` int(11) unsigned NOT NULL,
  `source_id` int(11) unsigned NOT NULL,
  `subject_academic_field_id` int(11) unsigned NOT NULL,
  `subject_associated_places_id` int(11) unsigned NOT NULL,
  `subject_other_id` int(11) unsigned NOT NULL,
  `subject_people_id` int(11) unsigned NOT NULL,
  `subject_place_id` int(11) unsigned NOT NULL,
  `subject_season_id` int(11) unsigned NOT NULL,
  `title_id` int(11) unsigned NOT NULL,
  `type_id` int(11) unsigned NOT NULL,
  `role_id` int(11) unsigned NOT NULL,
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`entry_id`),
  UNIQUE KEY `identifier_id` (`identifier_id`),
  KEY `bibliographic_citation_id` (`bibliographic_citation_id`),
  KEY `content_id` (`content_id`),
  KEY `content_url_id` (`content_url_id`),
  KEY `contributor_id` (`contributor_id`),
  KEY `country_id` (`country_id`),
  KEY `coverage_lat_id` (`coverage_lat_id`),
  KEY `coverage_long_id` (`coverage_long_id`),
  KEY `creator_id` (`creator_id`),
  KEY `creator_other_id` (`creator_other_id`),
  KEY `date_digital_id` (`date_digital_id`),
  KEY `date_exact_id` (`date_exact_id`),
  KEY `date_season_id` (`date_season_id`),
  KEY `date_season_yyyy_id` (`date_season_yyyy_id`),
  KEY `description_id` (`description_id`),
  KEY `digitization_specifications_id` (`digitization_specifications_id`),
  KEY `format_id` (`format_id`),
  KEY `language_id` (`language_id`),
  KEY `publisher_id` (`publisher_id`),
  KEY `publisher_location_id` (`publisher_location_id`),
  KEY `relation_id` (`relation_id`),
  KEY `rights_id` (`rights_id`),
  KEY `source_id` (`source_id`),
  KEY `subject_academic_field_id` (`subject_academic_field_id`),
  KEY `subject_associated_places_id` (`subject_associated_places_id`),
  KEY `subject_other_id` (`subject_other_id`),
  KEY `subject_people_id` (`subject_people_id`),
  KEY `subject_place_id` (`subject_place_id`),
  KEY `subject_season_id` (`subject_season_id`),
  KEY `type_id` (`type_id`),
  KEY `fk_title` (`title_id`),
  KEY `fk_content_url_audio` (`content_url_audio_id`),
  KEY `fk_content_url_transcript` (`content_url_transcript_id`),
  KEY `fk_role` (`role_id`),
  CONSTRAINT `entry_ibfk_1` FOREIGN KEY (`identifier_id`) REFERENCES `identifier` (`identifier_id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_bibliographic_citation` FOREIGN KEY (`bibliographic_citation_id`) REFERENCES `bibliographic_citation` (`bibliographic_citation_id`),
  CONSTRAINT `fk_content` FOREIGN KEY (`content_id`) REFERENCES `content` (`content_id`),
  CONSTRAINT `fk_content_url` FOREIGN KEY (`content_url_id`) REFERENCES `content_url` (`content_url_id`),
  CONSTRAINT `fk_content_url_audio` FOREIGN KEY (`content_url_audio_id`) REFERENCES `content_url` (`content_url_id`),
  CONSTRAINT `fk_content_url_transcript` FOREIGN KEY (`content_url_transcript_id`) REFERENCES `content_url` (`content_url_id`),
  CONSTRAINT `fk_contributor` FOREIGN KEY (`contributor_id`) REFERENCES `person` (`person_id`),
  CONSTRAINT `fk_country` FOREIGN KEY (`country_id`) REFERENCES `place` (`place_id`),
  CONSTRAINT `fk_coverage_lat` FOREIGN KEY (`coverage_lat_id`) REFERENCES `coverage_lat` (`coverage_lat_id`),
  CONSTRAINT `fk_coverage_long` FOREIGN KEY (`coverage_long_id`) REFERENCES `coverage_long` (`coverage_long_id`),
  CONSTRAINT `fk_creator` FOREIGN KEY (`creator_id`) REFERENCES `person` (`person_id`),
  CONSTRAINT `fk_creator_other` FOREIGN KEY (`creator_other_id`) REFERENCES `person` (`person_id`),
  CONSTRAINT `fk_date_digital` FOREIGN KEY (`date_digital_id`) REFERENCES `season` (`season_id`),
  CONSTRAINT `fk_date_exact` FOREIGN KEY (`date_exact_id`) REFERENCES `season` (`season_id`),
  CONSTRAINT `fk_date_season` FOREIGN KEY (`date_season_id`) REFERENCES `season` (`season_id`),
  CONSTRAINT `fk_date_season_yyyy` FOREIGN KEY (`date_season_yyyy_id`) REFERENCES `season` (`season_id`),
  CONSTRAINT `fk_description` FOREIGN KEY (`description_id`) REFERENCES `description` (`description_id`),
  CONSTRAINT `fk_digitization_specifications` FOREIGN KEY (`digitization_specifications_id`) REFERENCES `digitization_specifications` (`digitization_specifications_id`),
  CONSTRAINT `fk_format` FOREIGN KEY (`format_id`) REFERENCES `format` (`format_id`),
  CONSTRAINT `fk_language` FOREIGN KEY (`language_id`) REFERENCES `language` (`language_id`),
  CONSTRAINT `fk_publisher` FOREIGN KEY (`publisher_id`) REFERENCES `publisher` (`publisher_id`),
  CONSTRAINT `fk_relation` FOREIGN KEY (`relation_id`) REFERENCES `relation` (`relation_id`),
  CONSTRAINT `fk_rights` FOREIGN KEY (`rights_id`) REFERENCES `rights` (`rights_id`),
  CONSTRAINT `fk_role` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`),
  CONSTRAINT `fk_source` FOREIGN KEY (`source_id`) REFERENCES `source` (`source_id`),
  CONSTRAINT `fk_subject_academic_field` FOREIGN KEY (`subject_academic_field_id`) REFERENCES `subject_academic_field` (`subject_academic_field_id`),
  CONSTRAINT `fk_subject_associated_places` FOREIGN KEY (`subject_associated_places_id`) REFERENCES `place` (`place_id`),
  CONSTRAINT `fk_subject_other` FOREIGN KEY (`subject_other_id`) REFERENCES `subject_other` (`subject_other_id`),
  CONSTRAINT `fk_subject_people` FOREIGN KEY (`subject_people_id`) REFERENCES `person` (`person_id`),
  CONSTRAINT `fk_subject_place` FOREIGN KEY (`subject_place_id`) REFERENCES `place` (`place_id`),
  CONSTRAINT `fk_subject_season` FOREIGN KEY (`subject_season_id`) REFERENCES `season` (`season_id`),
  CONSTRAINT `fk_title` FOREIGN KEY (`title_id`) REFERENCES `title` (`title_id`),
  CONSTRAINT `fk_type` FOREIGN KEY (`type_id`) REFERENCES `type` (`type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table format
# ------------------------------------------------------------

DROP TABLE IF EXISTS `format`;

CREATE TABLE `format` (
  `format_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `format` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`format_id`),
  UNIQUE KEY `format` (`format`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table identifier
# ------------------------------------------------------------

DROP TABLE IF EXISTS `identifier`;

CREATE TABLE `identifier` (
  `identifier_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `identifier` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`identifier_id`),
  UNIQUE KEY `identifier` (`identifier`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table language
# ------------------------------------------------------------

DROP TABLE IF EXISTS `language`;

CREATE TABLE `language` (
  `language_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `language` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`language_id`),
  UNIQUE KEY `language` (`language`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table person
# ------------------------------------------------------------

DROP TABLE IF EXISTS `person`;

CREATE TABLE `person` (
  `person_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `person` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `first_name` mediumtext COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `last_name` mediumtext COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`person_id`),
  UNIQUE KEY `person` (`person`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table place
# ------------------------------------------------------------

DROP TABLE IF EXISTS `place`;

CREATE TABLE `place` (
  `place_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `place` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`place_id`),
  UNIQUE KEY `place` (`place`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table publisher
# ------------------------------------------------------------

DROP TABLE IF EXISTS `publisher`;

CREATE TABLE `publisher` (
  `publisher_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `publisher` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`publisher_id`),
  UNIQUE KEY `publisher` (`publisher`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table relation
# ------------------------------------------------------------

DROP TABLE IF EXISTS `relation`;

CREATE TABLE `relation` (
  `relation_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `relation` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`relation_id`),
  UNIQUE KEY `relation` (`relation`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table rights
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rights`;

CREATE TABLE `rights` (
  `rights_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `rights` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`rights_id`),
  UNIQUE KEY `rights` (`rights`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table role
# ------------------------------------------------------------

DROP TABLE IF EXISTS `role`;

CREATE TABLE `role` (
  `role_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `role` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`role_id`),
  UNIQUE KEY `role` (`role`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table season
# ------------------------------------------------------------

DROP TABLE IF EXISTS `season`;

CREATE TABLE `season` (
  `season_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `season` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`season_id`),
  UNIQUE KEY `season` (`season`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table source
# ------------------------------------------------------------

DROP TABLE IF EXISTS `source`;

CREATE TABLE `source` (
  `source_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `source` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`source_id`),
  UNIQUE KEY `source` (`source`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table subject_academic_field
# ------------------------------------------------------------

DROP TABLE IF EXISTS `subject_academic_field`;

CREATE TABLE `subject_academic_field` (
  `subject_academic_field_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `subject_academic_field` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`subject_academic_field_id`),
  UNIQUE KEY `subject_academic_field` (`subject_academic_field`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table subject_other
# ------------------------------------------------------------

DROP TABLE IF EXISTS `subject_other`;

CREATE TABLE `subject_other` (
  `subject_other_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `subject_other` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`subject_other_id`),
  UNIQUE KEY `subject_other` (`subject_other`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table title
# ------------------------------------------------------------

DROP TABLE IF EXISTS `title`;

CREATE TABLE `title` (
  `title_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`title_id`),
  UNIQUE KEY `title` (`title`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table type
# ------------------------------------------------------------

DROP TABLE IF EXISTS `type`;

CREATE TABLE `type` (
  `type_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `type` mediumtext COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`type_id`),
  UNIQUE KEY `type` (`type`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



# Dump of table whole_tsv_dump
# ------------------------------------------------------------

DROP TABLE IF EXISTS `whole_tsv_dump`;

CREATE TABLE `whole_tsv_dump` (
  `whole_tsv_dump_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `created` datetime DEFAULT current_timestamp(),
  `identifier_id` int(11) unsigned NOT NULL DEFAULT 0,
  `title_id` int(11) unsigned NOT NULL DEFAULT 0,
  `content_id` int(11) unsigned NOT NULL DEFAULT 0,
  `content_url_id` int(11) unsigned NOT NULL DEFAULT 0,
  `content_url_audio_id` int(11) unsigned NOT NULL DEFAULT 0,
  `content_url_transcript_id` int(11) unsigned NOT NULL DEFAULT 0,
  `creator_id` int(11) unsigned NOT NULL DEFAULT 0,
  `creator_other_id` int(11) unsigned NOT NULL DEFAULT 0,
  `subject_place_id` int(11) unsigned NOT NULL DEFAULT 0,
  `coverage_lat_id` int(11) unsigned NOT NULL DEFAULT 0,
  `coverage_long_id` int(11) unsigned NOT NULL DEFAULT 0,
  `subject_associated_places_id` int(11) unsigned NOT NULL DEFAULT 0,
  `subject_people_id` int(11) unsigned NOT NULL DEFAULT 0,
  `subject_academic_field_id` int(11) unsigned NOT NULL DEFAULT 0,
  `subject_other_id` int(11) unsigned NOT NULL DEFAULT 0,
  `subject_season_id` int(11) unsigned NOT NULL DEFAULT 0,
  `date_season_id` int(11) unsigned NOT NULL DEFAULT 0,
  `date_season_yyyy_id` int(11) unsigned NOT NULL DEFAULT 0,
  `date_exact_id` int(11) unsigned NOT NULL DEFAULT 0,
  `date_digital_id` int(11) unsigned NOT NULL DEFAULT 0,
  `description_id` int(11) unsigned NOT NULL DEFAULT 0,
  `format_id` int(11) unsigned NOT NULL DEFAULT 0,
  `digitization_specifications_id` int(11) unsigned NOT NULL DEFAULT 0,
  `contributor_id` int(11) unsigned NOT NULL DEFAULT 0,
  `type_id` int(11) unsigned NOT NULL DEFAULT 0,
  `country_id` int(11) unsigned NOT NULL DEFAULT 0,
  `language_id` int(11) unsigned NOT NULL DEFAULT 0,
  `relation_id` int(11) unsigned NOT NULL DEFAULT 0,
  `source_id` int(11) unsigned NOT NULL DEFAULT 0,
  `publisher_id` int(11) unsigned NOT NULL DEFAULT 0,
  `publisher_location_id` int(11) unsigned NOT NULL DEFAULT 0,
  `bibliographic_citation_id` int(11) unsigned NOT NULL DEFAULT 0,
  `rights_id` int(11) unsigned NOT NULL DEFAULT 0,
  `identifier` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `title` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `content` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `content_url` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `content_url_audio` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `content_url_transcript` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `creator` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `creator_other` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `subject_place` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `coverage_lat` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `coverage_long` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `subject_associated_places` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `subject_people` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `subject_academic_field` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `subject_other` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `subject_season` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `date_season` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `date_season_yyyy` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `date_exact` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `date_digital` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `description` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `format` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `digitization_specifications` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `contributor` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `type` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `country` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `language` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `relation` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `source` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `publisher` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `publisher_location` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `bibliographic_citation` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `rights` text COLLATE utf8mb4_unicode_520_ci DEFAULT '',
  `combined` text COLLATE utf8mb4_unicode_520_ci NOT NULL,
  PRIMARY KEY (`whole_tsv_dump_id`),
  UNIQUE KEY `all_tsv_fields` (`combined`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
