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
-- Table structure for table `cases`
--

DROP TABLE IF EXISTS `cases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cases` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(48) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cases`
--

LOCK TABLES `cases` WRITE;
/*!40000 ALTER TABLE `cases` DISABLE KEYS */;
INSERT INTO `cases` VALUES (0,'advection_quad'),(1,'advection_tri'),(2,'advection_hex'),(3,'advection_pris_x'),(4,'advection_pris_y'),(5,'advection_pris_z'),(6,'diffusion_quad'),(7,'diffusion_tri'),(8,'diffusion_hex'),(9,'diffusion_pris_x'),(10,'difffusion_pris_y'),(11,'diffusion_pris_z'),(12,'line'),(13,'quad'),(14,'tri'),(15,'hex'),(16,'pris'),(17,'tet'),(18,'GROUNDWATER_FLOW_quad'),(19,'GROUNDWATER_FLOW_tri'),(20,'LIQUID_FLOW_quad'),(21,'LIQUID_FLOW_tri'),(22,'1_1_1'),(23,'1_1_2'),(24,'1_2_1'),(25,'2_1_1'),(26,'2_1_2'),(27,'2_2_1'),(28,'HEAT_TRANSPORT_quad'),(29,'MASS_TRANSPORT_quad'),(30,'haline'),(31,'thermal'),(32,'thermohaline'),(33,'line_LIQUID_FLOW_LPVC'),(34,'line_LIQUID_FLOW_REFERENCE'),(35,'line_HEAT_TRANSPORT_advective_LPVC'),(36,'line_HEAT_TRANSPORT_advective_REFERENCE'),(37,'line_HEAT_TRANSPORT_diffusive_LPVC'),(38,'line_HEAT_TRANSPORT_diffusive_REFERENCE'),(39,'quad_LIQUID_FLOW_LPVC'),(40,'quad_LIQUID_FLOW_REFERENCE'),(41,'quad_HEAT_TRANSPORT_advective_LPVC'),(42,'quad_HEAT_TRANSPORT_advective_REFERENCE'),(43,'quad_HEAT_TRANSPORT_diffusive_LPVC'),(44,'quad_HEAT_TRANSPORT_diffusive_REFERENCE'),(45,'advective'),(46,'diffusive');
/*!40000 ALTER TABLE `cases` ENABLE KEYS */;
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
