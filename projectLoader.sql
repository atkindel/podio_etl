DROP TABLE IF EXISTS `CourseIDMap`;
CREATE TABLE `CourseIDMap` (
  `course_display_name` varchar(50) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `CourseVitals`;
CREATE TABLE `CourseVitals` (
  `project_id` int(11) DEFAULT NULL,
  `project_name` varchar(50) DEFAULT NULL,
  `school` varchar(50) DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL,
  `institute` varchar(50) DEFAULT NULL,
  `faculty_name` varchar(50) DEFAULT NULL,
  `faculty_org` varchar(50) DEFAULT NULL,
  `faculty-title` varchar(50) DEFAULT NULL,
  `platform` varchar(50) DEFAULT NULL,
  `stanford-course` varchar(50) DEFAULT NULL,
  `quarter-offered` varchar(50) DEFAULT NULL,
  `duration` varchar(50) DEFAULT NULL,
  `exemplary-course3` varchar(50) DEFAULT NULL,
  `delivery-format` varchar(50) DEFAULT NULL,
  `course-type` varchar(50) DEFAULT NULL,
  `course-offering-type` varchar(50) DEFAULT NULL,
  `course-level` varchar(50) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `CourseProduction`;
CREATE TABLE `CourseProduction` (
  `project_id` int(11) DEFAULT NULL,
  `vpol-priority` varchar(50) DEFAULT NULL,
  `engineering-support-level` varchar(50) DEFAULT NULL,
  `platform-support-level` varchar(50) DEFAULT NULL,
  `level-of-effort-id` varchar(50) DEFAULT NULL,
  `level-of-effort-production` varchar(50) DEFAULT NULL,
  `video-production-handling` varchar(50) DEFAULT NULL,
  `production-hours` varchar(50) DEFAULT NULL,
  `post-production-hours` varchar(50) DEFAULT NULL,
  `seed-grant` varchar(50) DEFAULT NULL,
  `funding-amount` int(11) DEFAULT NULL,
  `funding-source` varchar(50) DEFAULT NULL,
  `funding-stipulations` varchar(500) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
