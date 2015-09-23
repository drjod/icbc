-- MySQL dump 10.13  Distrib 5.6.24, for Win64 (x86_64)
--
-- Host: localhost    Database: testing_environment
-- ------------------------------------------------------
-- Server version	5.6.26-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `modi`
--

DROP TABLE IF EXISTS `modi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modi` (
  `id` int(11) NOT NULL,
  `computer_id` int(11) DEFAULT NULL,
  `configuration_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_idx` (`configuration_id`),
  KEY `computer_idx` (`computer_id`),
  CONSTRAINT `key_computer` FOREIGN KEY (`computer_id`) REFERENCES `computer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `modi_ibfk_1` FOREIGN KEY (`configuration_id`) REFERENCES `configurations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modi`
--

LOCK TABLES `modi` WRITE;
/*!40000 ALTER TABLE `modi` DISABLE KEYS */;
INSERT INTO `modi` VALUES (0,0,0),(1,0,1),(2,4,0),(3,4,1),(4,1,0),(5,1,1),(6,1,2),(7,1,3),(8,1,4),(9,1,5),(10,2,0),(11,2,1),(12,2,2),(13,2,3),(14,2,4),(15,2,5),(16,3,0),(17,3,1),(18,3,2),(19,3,3),(20,3,4),(21,3,5);
/*!40000 ALTER TABLE `modi` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-09-23 14:54:25
