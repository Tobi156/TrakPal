/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.6.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: career_tracker
-- ------------------------------------------------------
-- Server version	11.6.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `careermatches`
--

DROP TABLE IF EXISTS `careermatches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `careermatches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `career_id` int(11) DEFAULT NULL,
  `major` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `career_id` (`career_id`),
  CONSTRAINT `careermatches_ibfk_1` FOREIGN KEY (`career_id`) REFERENCES `careerrecommendations` (`career_id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `careermatches`
--

LOCK TABLES `careermatches` WRITE;
/*!40000 ALTER TABLE `careermatches` DISABLE KEYS */;
INSERT INTO `careermatches` VALUES
(34,14,'Computer Science'),
(35,15,'Psychology'),
(36,16,'Business Administration'),
(37,16,'Computer Science'),
(38,17,'Biology'),
(39,18,'Computer Science'),
(40,18,'Biology'),
(41,19,'Psychology'),
(42,19,'Business Administration'),
(43,20,'Biology'),
(44,21,'Computer Science'),
(45,22,'Business Administration'),
(46,23,'Psychology'),
(47,23,'Biology');
/*!40000 ALTER TABLE `careermatches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `careerrecommendations`
--

DROP TABLE IF EXISTS `careerrecommendations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `careerrecommendations` (
  `career_id` int(11) NOT NULL AUTO_INCREMENT,
  `min_gpa` decimal(3,2) NOT NULL CHECK (`min_gpa` between 0 and 4.0),
  `career_name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`career_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `careerrecommendations`
--

LOCK TABLES `careerrecommendations` WRITE;
/*!40000 ALTER TABLE `careerrecommendations` DISABLE KEYS */;
INSERT INTO `careerrecommendations` VALUES
(14,3.00,'Software Engineer','Designs and builds software applications and systems.','https://raw.githubusercontent.com/Tobi156/TrakPal/main/backend/resources/softwareEngStock.jpg'),
(15,3.20,'Clinical Psychologist','Works with patients to diagnose and treat mental disorders.','https://raw.githubusercontent.com/Tobi156/TrakPal/main/backend/resources/ClinPsyStock.jpg'),
(16,2.80,'Marketing Analyst','Analyzes marketing trends and campaign performance.','https://raw.githubusercontent.com/Tobi156/TrakPal/main/backend/resources/markAnaStock.jpg'),
(17,3.00,'Biotech Lab Technician','Conducts lab tests in biotechnology or medical research.','https://raw.githubusercontent.com/Tobi156/TrakPal/main/backend/resources/BioLabTechStock.jpg'),
(18,3.00,'Data Scientist','Extracts insights from large datasets using statistical tools.','https://raw.githubusercontent.com/Tobi156/TrakPal/main/backend/resources/DataSciStock.jpg'),
(19,2.50,'HR Coordinator','Manages administrative tasks in the human resources department.','https://raw.githubusercontent.com/Tobi156/TrakPal/main/backend/resources/HRCordStock.jpg'),
(20,3.20,'Genetic Counselor','Assesses genetic risks and explains test results to patients.','https://raw.githubusercontent.com/Tobi156/TrakPal/main/backend/resources/GenCounStock.jpg'),
(21,2.70,'IT Support Specialist','Provides technical support and system troubleshooting.','https://raw.githubusercontent.com/Tobi156/TrakPal/main/backend/resources/ITSuppStock.jpg'),
(22,2.80,'Operations Manager','Oversees daily operations to improve efficiency.','https://raw.githubusercontent.com/Tobi156/TrakPal/main/backend/resources/OpManStock.jpg'),
(23,3.00,'Research Assistant','Assists in academic or clinical research projects.','https://raw.githubusercontent.com/Tobi156/TrakPal/main/backend/resources/ResAssStock.jpg');
/*!40000 ALTER TABLE `careerrecommendations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courses` (
  `course_id` int(11) NOT NULL AUTO_INCREMENT,
  `course_name` varchar(255) NOT NULL,
  `course_code` varchar(50) NOT NULL,
  `credits` int(11) NOT NULL CHECK (`credits` > 0),
  `difficulty_level` enum('Easy','Medium','Hard') DEFAULT 'Medium',
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`course_id`),
  UNIQUE KEY `course_code` (`course_code`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `grades`
--

DROP TABLE IF EXISTS `grades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grades` (
  `grade_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `grade` char(2) NOT NULL,
  `semester` varchar(20) DEFAULT NULL,
  `year` int(11) DEFAULT NULL CHECK (`year` >= 2000),
  PRIMARY KEY (`grade_id`),
  KEY `user_id` (`user_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `grades_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `grades_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE,
  CONSTRAINT `grades_chk_valid_grade` CHECK (`grade` in ('A','A-','A+','B','B-','B+','C','C-','C+','D','D-','D+','F'))
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `requiredcourses`
--

DROP TABLE IF EXISTS `requiredcourses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `requiredcourses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `major` varchar(100) DEFAULT NULL,
  `course_code` varchar(20) DEFAULT NULL,
  `course_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requiredcourses`
--

LOCK TABLES `requiredcourses` WRITE;
/*!40000 ALTER TABLE `requiredcourses` DISABLE KEYS */;
INSERT INTO `requiredcourses` VALUES
(1,'Computer Science','CISC 1115','Introduction to Programming'),
(2,'Computer Science','CISC 1170','Introduction to Computer Systems'),
(3,'Computer Science','CISC 3115','Advanced Programming Techniques'),
(4,'Computer Science','CISC 3130','Data Structures'),
(5,'Computer Science','CISC 3140','Software Engineering'),
(6,'Computer Science','CISC 3220','Algorithms'),
(7,'Computer Science','CISC 3310','Principles of Programming Languages'),
(8,'Computer Science','CISC 3320','Operating Systems'),
(9,'Computer Science','CISC 3340','Computer Architecture'),
(10,'Computer Science','CISC 4900','Senior Project'),
(11,'Psychology','PSYC 1000','Introduction to Psychology'),
(12,'Psychology','PSYC 2000W','Experimental Psychology'),
(13,'Psychology','PSYC 2100','Psychological Statistics'),
(14,'Psychology','PSYC 2600','Brain and Behavior'),
(15,'Psychology','PSYC 3400','Cognitive Psychology'),
(16,'Business Administration','ACCT 2001','Principles of Accounting I'),
(17,'Business Administration','ACCT 2002','Principles of Accounting II'),
(18,'Business Administration','BUSN 2100','Business Law I'),
(19,'Business Administration','BUSN 3200','Principles of Management'),
(20,'Business Administration','BUSN 3400','Marketing Principles'),
(21,'Business Administration','ECON 2100','Microeconomics'),
(22,'Business Administration','ECON 2200','Macroeconomics'),
(23,'Business Administration','MATH 1201','Calculus I'),
(24,'Business Administration','BUSN 3100','Business Statistics'),
(25,'Biology','BIOL 1001','General Biology I'),
(26,'Biology','BIOL 1002','General Biology II'),
(27,'Biology','CHEM 1100','General Chemistry I'),
(28,'Biology','CHEM 1200','General Chemistry II'),
(29,'Biology','CHEM 2100','Organic Chemistry I'),
(30,'Biology','CHEM 2200','Organic Chemistry II'),
(31,'Biology','PHYS 1100','General Physics I'),
(32,'Biology','PHYS 1200','General Physics II'),
(33,'Biology','MATH 1201','Calculus I');
/*!40000 ALTER TABLE `requiredcourses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `major` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `is_admin` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-05-10  0:57:30
