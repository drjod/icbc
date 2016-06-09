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
-- Table structure for table `examples`
--

DROP TABLE IF EXISTS `examples`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `examples` (
  `id` int(11) NOT NULL DEFAULT '0',
  `type_id` int(11) NOT NULL,
  `case_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `type_id_idx` (`type_id`),
  KEY `case_id` (`case_id`),
  CONSTRAINT `examples_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `types` (`id`),
  CONSTRAINT `examples_ibfk_2` FOREIGN KEY (`case_id`) REFERENCES `cases` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `examples`
--

LOCK TABLES `examples` WRITE;
/*!40000 ALTER TABLE `examples` DISABLE KEYS */;
INSERT INTO `examples` VALUES (0,0,0),(1,0,1),(2,0,6),(3,0,7),(4,1,0),(5,1,1),(6,1,6),(7,1,7),(8,2,2),(9,2,5),(10,2,8),(11,2,11),(12,3,3),(13,3,4),(14,3,9),(15,3,10),(16,4,0),(17,4,1),(18,4,6),(19,4,7),(20,5,12),(21,5,13),(22,5,14),(23,5,15),(24,5,16),(25,5,17),(26,6,18),(27,6,19),(28,6,20),(29,6,21),(30,8,22),(31,8,23),(32,8,24),(33,8,25),(34,8,26),(35,8,27),(36,9,22),(37,9,23),(38,9,24),(39,9,25),(41,9,26),(42,9,27),(43,7,28),(44,7,29),(45,10,30),(46,10,31),(47,10,32),(48,11,33),(49,11,34),(50,11,35),(51,11,36),(52,11,37),(53,11,38),(54,11,39),(55,11,40),(56,11,41),(57,11,42),(58,11,43),(59,11,44),(60,12,39),(61,12,40),(62,12,41),(63,12,42),(64,12,43),(65,12,44),(66,13,45),(67,13,46),(68,14,15),(69,14,16),(70,15,15);
/*!40000 ALTER TABLE `examples` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-09-23 14:54:26
