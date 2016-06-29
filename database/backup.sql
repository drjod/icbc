-- MySQL dump 10.13  Distrib 5.6.24, for Win64 (x86_64)
--
-- Host: localhost    Database: testing_environment
-- ------------------------------------------------------
-- Server version	5.5.45

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
-- Table structure for table `branches`
--

DROP TABLE IF EXISTS `branches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `branches` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branches`
--

LOCK TABLES `branches` WRITE;
/*!40000 ALTER TABLE `branches` DISABLE KEYS */;
INSERT INTO `branches` VALUES (0,'ogs_kb1'),(1,'trunk'),(2,'ogs_cb_2016_5_19'),(3,'ogs_kb1_0.1.3_extended'),(4,'ogs_kiel_testing_2015_11_11'),(5,'trunk_2015_11_11'),(6,'kb1_0.2');
/*!40000 ALTER TABLE `branches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cases`
--

DROP TABLE IF EXISTS `cases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cases` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(45) DEFAULT NULL,
  `flow_id` varchar(50) DEFAULT NULL,
  `mass_flag` varchar(50) DEFAULT NULL,
  `heat_flag` varchar(50) DEFAULT NULL,
  `coupled_flag` varchar(50) DEFAULT NULL,
  `lumping_flow` varchar(50) DEFAULT NULL,
  `nonlinear_flag` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `theta_flow` varchar(50) DEFAULT NULL,
  `theta_heat` varchar(50) DEFAULT NULL,
  `theta_mass` varchar(50) DEFAULT NULL,
  `solver_flow_ogs_fem` varchar(50) DEFAULT NULL,
  `solver_flow_ogs_fem_sp` varchar(50) DEFAULT NULL,
  `solver_flow_ogs_fem_mkl` varchar(50) DEFAULT NULL,
  `solver_flow_ogs_fem_mpi` varchar(50) DEFAULT NULL,
  `solver_flow_ogs_fem_petsc` varchar(50) DEFAULT NULL,
  `solver_heat_ogs_fem` varchar(50) DEFAULT NULL,
  `solver_heat_ogs_fem_sp` varchar(50) DEFAULT NULL,
  `solver_heat_ogs_fem_mkl` varchar(50) DEFAULT NULL,
  `solver_heat_ogs_fem_mpi` varchar(50) DEFAULT NULL,
  `solver_heat_ogs_fem_petsc` varchar(50) DEFAULT NULL,
  `solver_mass_ogs_fem` varchar(50) DEFAULT NULL,
  `solver_mass_ogs_fem_sp` varchar(50) DEFAULT NULL,
  `solver_mass_ogs_fem_mkl` varchar(50) DEFAULT NULL,
  `solver_mass_ogs_fem_mpi` varchar(50) DEFAULT NULL,
  `solver_mass_ogs_fem_petsc` varchar(50) DEFAULT NULL,
  `preconditioner_flow_ogs_fem` varchar(50) DEFAULT NULL,
  `preconditioner_flow_ogs_fem_sp` varchar(50) DEFAULT NULL,
  `preconditioner_flow_ogs_fem_mkl` varchar(50) DEFAULT NULL,
  `preconditioner_flow_ogs_fem_mpi` varchar(50) DEFAULT NULL,
  `preconditioner_flow_ogs_fem_petsc` varchar(50) DEFAULT NULL,
  `preconditioner_heat_ogs_fem` varchar(50) DEFAULT NULL,
  `preconditioner_heat_ogs_fem_sp` varchar(50) DEFAULT NULL,
  `preconditioner_heat_ogs_fem_mkl` varchar(50) DEFAULT NULL,
  `preconditioner_heat_ogs_fem_mpi` varchar(50) DEFAULT NULL,
  `preconditioner_heat_ogs_fem_petsc` varchar(50) DEFAULT NULL,
  `preconditioner_mass_ogs_fem` varchar(50) DEFAULT NULL,
  `preconditioner_mass_ogs_fem_sp` varchar(50) DEFAULT NULL,
  `preconditioner_mass_ogs_fem_mkl` varchar(50) DEFAULT NULL,
  `preconditioner_mass_ogs_fem_mpi` varchar(50) DEFAULT NULL,
  `preconditioner_mass_ogs_fem_petsc` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cases`
--

LOCK TABLES `cases` WRITE;
/*!40000 ALTER TABLE `cases` DISABLE KEYS */;
INSERT INTO `cases` VALUES (0,'advection_quad_xy','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','2','1','1','0','1','1','1','1','0','1','1','1','1','0','1','1'),(1,'advection_tri_xy','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','2','1','1','0','1','1','1','1','0','1','1','1','1','0','1','1'),(2,'advection_hex','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','2','1','1','0','1','1','1','1','0','1','1','1','1','0','1','1'),(3,'advection_pris_x','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','2','1','1','0','1','1','1','1','0','1','1','1','1','0','1','1'),(4,'advection_pris_y','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','2','1','1','0','1','1','1','1','0','1','1','1','1','0','1','1'),(5,'advection_pris_z','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','2','1','1','0','1','1','1','1','0','1','1','1','1','0','1','1'),(6,'diffusion_quad_xy','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','1','1','1','1','0','1','1'),(7,'diffusion_tri_xy','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','1','1','1','1','0','1','1'),(8,'diffusion_hex','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','1','1','1','1','0','1','1'),(9,'diffusion_pris_x','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','1','1','1','1','0','1','1'),(10,'diffusion_pris_y','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','1','1','1','1','0','1','1'),(11,'diffusion_pris_z','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','1','1','1','1','0','1','1'),(12,'1D_line','2','1','0','0','1','0','1','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null','1','1','1','1','0','1','1'),(13,'1D_quad','2','1','0','0','1','0','1','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null','1','1','1','1','0','1','1'),(14,'1D_tri','2','1','0','0','1','0','1','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null','1','1','1','1','0','1','1'),(15,'1D_hex','2','1','0','0','1','0','1','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null','1','1','1','1','0','1','1'),(16,'1D_pris','2','1','0','0','1','0','1','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null','1','1','1','1','0','1','1'),(17,'1D_tet','2','1','0','0','1','0','1','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null','1','1','1','1','0','1','1'),(18,'GROUNDWATER_FLOW_quad','2','1','0','0','1','0','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null','1','1','1','1','0','1','1'),(19,'GROUNDWATER_FLOW_tri','2','1','0','0','1','0','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null','1','1','1','1','0','1','1'),(20,'LIQUID_FLOW_quad','1','1','0','0','1','0','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null','1','1','1','1','0','1','1'),(21,'LIQUID_FLOW_tri','1','1','0','0','1','0','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null','1','1','1','1','0','1','1'),(22,'1_1_1_hex','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(23,'1_1_2_hex','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(24,'1_2_1_hex','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(25,'2_1_1_hex','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(26,'2_1_2_hex','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(27,'2_2_1_hex','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(28,'MASS_TRANSPORT_quad','1','1','0','0','1','0','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null',NULL,NULL,'1','1','0','1','1'),(29,'HEAT_TRANSPORT_quad','1','0','1','0','1','0','0','1','1','null','2','2','0','2','0','2','2','0','2','0','null','null','null',NULL,NULL,'1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(30,'haline','1','1','0','1','1','1','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null',NULL,NULL,'1','1','0','1','1'),(31,'thermal','1','0','1','1','1','1','0','1','1','null','2','2','0','2','0','2','2','0','2','0','null','null','null',NULL,NULL,'1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(32,'thermohaline','1','1','1','1','1','1','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(33,'line_LIQUID_FLOW_LPVC','1','0','0','0','1','0','0','1','null','null','13','13','0','13','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(34,'line_LIQUID_FLOW_REFERENCE','1','0','0','0','1','0','0','1','null','null','13','13','0','13','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(35,'line_HEAT_TRANSPORT_advective_LPVC','1','0','1','0','1','0','0','1','1','null','13','13','0','13','0','13','13','0','13','0','null','null','null','13','0','1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(36,'line_HEAT_TRANSPORT_advective_REFERENCE','1','0','1','0','1','0','0','1','1','null','13','13','0','13','0','13','13','0','13','0','null','null','null','13','0','1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(37,'line_HEAT_TRANSPORT_diffusive_LPVC','1','0','1','0','1','0','0','1','1','null','13','13','0','13','0','13','13','0','13','0','null','null','null','13','0','1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(38,'line_HEAT_TRANSPORT_diffusive_REFERENCE','1','0','1','0','1','0','0','1','1','null','13','13','0','13','0','13','13','0','13','0','null','null','null','13','0','1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(39,'quad_LIQUID_FLOW_LPVC','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(40,'quad_LIQUID_FLOW_REFERENCE','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(41,'quad_HEAT_TRANSPORT_advective_LPVC','1','0','1','0','1','0','0','1','1','null','2','2','0','2','0','2','2','0','2','0','null','null','null',NULL,NULL,'1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(42,'quad_HEAT_TRANSPORT_advective_REFERENCE','1','0','1','0','1','0','0','1','1','null','2','2','0','2','0','2','2','0','2','0','null','null','null',NULL,NULL,'1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(43,'quad_HEAT_TRANSPORT_diffusive_LPVC','1','0','1','0','1','0','0','1','1','null','2','2','0','2','0','2','2','0','2','0','null','null','null',NULL,NULL,'1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(44,'quad_HEAT_TRANSPORT_diffusive_REFERENCE','1','0','1','0','1','0','0','1','1','null','2','2','0','2','0','2','2','0','2','0','null','null','null',NULL,NULL,'1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(45,'advective','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(46,'diffusive','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(47,'hex_HEAT_TRANSPORT','1','0','1','0','1','0','0','1','1','null','2','2','0','2','0','2','2','0','2','0','null','null','null',NULL,NULL,'1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(48,'pris_HEAT_TRANSPORT','1','0','1','0','1','0','0','1','1','null','2','2','0','2','0','2','2','0','2','0','null','null','null',NULL,NULL,'1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(49,'2D_xy','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(50,'2D_xy_LPVC','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(51,'2D_xz','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(52,'2D_xz_LPVC','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(53,'3D','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(54,'3D_LPVC','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(55,'Pc-Pnw','4','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(56,'P-S','5','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(57,'line_MULTI_PHASE_FLOW','4','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(58,'__quad_MULTI_PHASE_FLOW','4','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(59,'_tri_MULTI_PHASE_FLOW','4','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(60,'_hex_MULTI_PHASE_FLOW','4','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(61,'_tet_MULTI_PHASE_FLOW','4','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(62,'tri_MULTI_PHASE_DEFORMATION','4','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(63,'line_RICHARDS_FLOW','3','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(64,'II','1','0','1','0','1','0','0','1','1','null','2','2','0','2','0','2','2','0','2','0','null','null','null',NULL,NULL,'1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(65,'C','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(66,'cutOut_deactivatedSubdomain','1','0','1','1','1','1','0','1','1','null','2','2','0','2','0','2','2','0','2','0','null','null','null',NULL,NULL,'1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(67,'cutOut_materialDensity','1','0','1','1','1','1','0','1','1','null','2','2','0','2','0','2','2','0','2','0','null','null','null',NULL,NULL,'1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(68,'decay','1','1','0','0','1','0','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null',NULL,NULL,'1','1','0','1','1'),(69,'calcite','2','1','0','0','1','0','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null',NULL,NULL,'1','1','0','1','1'),(70,'line_PS_GLOBAL','5','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(71,'quad_PS_GLOBAL','5','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(72,'tri_PS_GLOBAL','5','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(73,'hex_PS_GLOBAL','5','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(74,'pris_PS_GLOBAL','5','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(75,'tet_PS_GLOBAL','5','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(76,'line_PS_GLOBAL_MASS','5','1','0','0','1','1','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null',NULL,NULL,'1','1','0','1','1'),(77,'quad_PS_GLOBAL_MASS','5','1','0','0','1','1','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null',NULL,NULL,'1','1','0','1','1'),(78,'tri_PS_GLOBAL_MASS','5','1','0','0','1','1','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null',NULL,NULL,'1','1','0','1','1'),(79,'hex_PS_GLOBAL_MASS','5','1','0','0','1','1','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null',NULL,NULL,'1','1','0','1','1'),(80,'pris_PS_GLOBAL_MASS','5','1','0','0','1','1','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null',NULL,NULL,'1','1','0','1','1'),(81,'tet_PS_GLOBAL_MASS','5','1','0','0','1','1','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null',NULL,NULL,'1','1','0','1','1'),(82,'kinReact','5','1','0','0','1','1','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null',NULL,NULL,'1','1','0','1','1'),(83,'cc','1','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(84,'dyn','1','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(85,'tri','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(86,'foot_tri','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(87,'foot_tet','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(88,'linearSwelling','3','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(89,'excavation','1','0','0','1','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(90,'unsaturated','3','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(91,'decovalex_2015_b2s1','3','1','1','1','1','1','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(92,'faults','1','1','0','0','1','0','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null',NULL,NULL,'1','1','0','1','1'),(93,'fractures','1','0','1','0','1','1','0','1','1','null','2','2','0','2','0','2','2','0','2','0','null','null','null',NULL,NULL,'1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(94,'inclined_line','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null','0','1','null','null','null','1','1'),(95,'inclined_quad','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,'null','null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(96,'lauwerier','1','0','1','0','1','1','0','1','1','null','2','2','0','2','0','2','2','0','2','0','null','null','null',NULL,NULL,'1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(97,'SUPG_steady','1','0','1','0','1','1','0','1','1','null','2','2','0','2','0','2','2','0','2','0','null','null','null',NULL,NULL,'1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(98,'SUPG_transient','1','0','1','0','1','1','0','1','1','null','2','2','0','2','0','2','2','0','2','0','null','null','null','2','0','1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(99,'FEM_FCT','1','1','0','0','1','0','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null','0','1','1','1','0','1','1'),(100,'CO2_dissolution','1','1','0','1','1','1','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null',NULL,NULL,'1','1','0','1','1'),(101,'nitrate','2','1','0','0','1','0','0','1','null','1','2','2','0','2','0','null','null','null',NULL,NULL,'2','2','0','2','0','1','1','0','1','1','null','null','null',NULL,NULL,'1','1','0','1','1'),(102,'advection_quad_xz','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(103,'advection_tri_xz','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(104,'advection_quad_axis','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(105,'advection_tri_axis','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(106,'diffusion_quad_xz','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(107,'diffusion_tri_xz','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(108,'diffusion_quad_axis','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(109,'diffusion_tri_axis','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(110,'1_1_1_pris','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(111,'1_1_2_pris','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(112,'1_2_1_pris','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','1','1','1','1','0','1','1'),(113,'2_1_1_pris','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(114,'2_1_2_pris','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(115,'2_2_1_pris','1','1','1','0','1','0','0','1','1','1','2','2','0','2','0','2','2','0','2','0','2','2','0','2','0','1','1','0','1','1','1','1','0','0','1','1','1','0','1','1'),(116,'quad_LIQUID_FLOW_LPVC','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(117,'quad_LIQUID_FLOW_REFERENCE','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(118,'quad_HEAT_TRANSPORT_advective_LPVC','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(119,'quad_HEAT_TRANSPORT_advective_REFERENCE','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(120,'quad_HEAT_TRANSPORT_diffusive_LPVC','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(121,'quad_HEAT_TRANSPORT_diffusive_REFERENC','1','0','0','0','1','0','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(122,'hex_HEAT_TRANSPORT','1','0','1','0','1','0','0','1','1','null','2','2','0','2','0','2','2','0','2',NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','1','1','0','0','1','null','null','null','1','1'),(123,'__line_MULTI_PHASE_FLOW','4','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(124,'_line_MULTI_PHASE_FLOW','4','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(125,'_quad_MULTI_PHASE_FLOW','4','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1'),(126,'line_RICHARDS_FLOW','3','0','0','0','1','1','0','1','null','null','2','2','0','2','0','null','null','null',NULL,NULL,'null','null','null',NULL,NULL,'1','1','0','1','1','null','null','null',NULL,NULL,'null','null','null','1','1');
/*!40000 ALTER TABLE `cases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `codes`
--

DROP TABLE IF EXISTS `codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `codes` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `codes`
--

LOCK TABLES `codes` WRITE;
/*!40000 ALTER TABLE `codes` DISABLE KEYS */;
INSERT INTO `codes` VALUES (0,'ogs');
/*!40000 ALTER TABLE `codes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `computer`
--

DROP TABLE IF EXISTS `computer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `computer` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(45) DEFAULT NULL,
  `operating_system` varchar(45) DEFAULT NULL,
  `location` varchar(45) DEFAULT NULL,
  `hostname` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `computer`
--

LOCK TABLES `computer` WRITE;
/*!40000 ALTER TABLE `computer` DISABLE KEYS */;
INSERT INTO `computer` VALUES (0,'amak','windows','local','*****'),(1,'rzcluster','linux','remote','rzcluster.rz.uni-kiel.de'),(2,'NEC','linux','remote','nesh-fe.rz.uni-kiel.de'),(3,'Lokstedt','linux','remote','134.245.120.191'),(4,'ibiza','windows','local','*****');
/*!40000 ALTER TABLE `computer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configurations`
--

DROP TABLE IF EXISTS `configurations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configurations` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(45) DEFAULT NULL,
  `processing` varchar(45) DEFAULT NULL,
  `preconditioner_table_name` varchar(50) DEFAULT NULL,
  `solver_table_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configurations`
--

LOCK TABLES `configurations` WRITE;
/*!40000 ALTER TABLE `configurations` DISABLE KEYS */;
INSERT INTO `configurations` VALUES (0,'OGS_FEM','sequential','preconditioner','solver'),(1,'OGS_FEM_SP','sequential','preconditioner','solver'),(2,'OGS_FEM_MKL','omp','preconditioner_mkl','solver_mkl'),(3,'OGS_FEM_MPI','mpi_elements','preconditioner','solver'),(4,'OGS_FEM_PETSC','mpi_nodes','preconditioner_petsc','solver_petsc');
/*!40000 ALTER TABLE `configurations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `examples`
--

DROP TABLE IF EXISTS `examples`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `examples` (
  `id` int(11) NOT NULL DEFAULT '0',
  `type_id` varchar(45) DEFAULT NULL,
  `case_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `examples`
--

LOCK TABLES `examples` WRITE;
/*!40000 ALTER TABLE `examples` DISABLE KEYS */;
INSERT INTO `examples` VALUES (0,'0','0'),(1,'0','1'),(2,'0','6'),(3,'0','7'),(4,'1','102'),(5,'1','103'),(6,'1','106'),(7,'1','107'),(8,'2','2'),(9,'2','5'),(10,'2','8'),(11,'2','11'),(12,'3','3'),(13,'3','4'),(14,'3','9'),(15,'3','10'),(16,'4','104'),(17,'4','105'),(18,'4','108'),(19,'4','109'),(20,'5','12'),(21,'5','13'),(22,'5','14'),(23,'5','15'),(24,'5','16'),(25,'5','17'),(26,'6','18'),(27,'6','19'),(28,'6','20'),(29,'6','21'),(30,'8','22'),(31,'8','23'),(32,'8','24'),(33,'8','25'),(34,'8','26'),(35,'8','27'),(36,'9','110'),(37,'9','111'),(38,'9','112'),(39,'9','113'),(40,'9','114'),(41,'9','115'),(42,'7','28'),(43,'10','30'),(44,'10','31'),(45,'10','32'),(46,'11','33'),(47,'11','34'),(48,'11','35'),(49,'11','36'),(50,'11','37'),(51,'11','38'),(52,'11','39'),(53,'11','40'),(54,'11','41'),(55,'11','42'),(56,'11','43'),(57,'11','44'),(58,'12','116'),(59,'12','117'),(60,'12','118'),(61,'12','119'),(62,'12','120'),(63,'12','121'),(64,'13','45'),(65,'13','46'),(66,'14','47'),(67,'14','48'),(68,'15','122'),(69,'7','29'),(70,'16','49'),(71,'16','50'),(72,'16','51'),(73,'16','52'),(74,'16','53'),(75,'16','54'),(76,'17','55'),(77,'17','56'),(78,'18','57'),(79,'19','123'),(80,'19','58'),(81,'20','124'),(82,'20','125'),(83,'20','59'),(84,'20','60'),(85,'20','61'),(86,'21','62'),(87,'22','63'),(88,'23','126'),(89,'24','64'),(90,'24','65'),(91,'24','66'),(92,'24','67'),(93,'25','68'),(94,'25','69'),(95,'26','70'),(96,'26','71'),(97,'26','72'),(98,'26','73'),(99,'26','74'),(100,'26','75'),(101,'26','76'),(102,'26','77'),(103,'26','78'),(104,'26','79'),(105,'26','80'),(106,'26','81'),(107,'26','82'),(108,'27','83'),(109,'27','84'),(110,'27','85'),(111,'27','86'),(112,'27','87'),(113,'27','88'),(114,'27','89'),(115,'27','90'),(116,'28','91'),(117,'29','92'),(118,'29','93'),(119,'29','94'),(120,'29','95'),(121,'29','96'),(122,'29','97'),(123,'29','98'),(124,'29','99'),(125,'25','100'),(126,'25','101');
/*!40000 ALTER TABLE `examples` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flow_processes`
--

DROP TABLE IF EXISTS `flow_processes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flow_processes` (
  `id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flow_processes`
--

LOCK TABLES `flow_processes` WRITE;
/*!40000 ALTER TABLE `flow_processes` DISABLE KEYS */;
INSERT INTO `flow_processes` VALUES (0,'NO_FLOW'),(1,'LIQUID_FLOW'),(2,'GROUNDWATER_FLOW'),(3,'RICHARDS_FLOW'),(4,'MULTI_PHASE_FLOW'),(5,'PS_GLOBAL'),(6,'DEFORMATION_FLOW');
/*!40000 ALTER TABLE `flow_processes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modi`
--

DROP TABLE IF EXISTS `modi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modi` (
  `id` int(11) NOT NULL DEFAULT '0',
  `computer_id` varchar(45) DEFAULT NULL,
  `configuration_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modi`
--

LOCK TABLES `modi` WRITE;
/*!40000 ALTER TABLE `modi` DISABLE KEYS */;
INSERT INTO `modi` VALUES (0,'0','0'),(1,'0','1'),(2,'4','0'),(3,'4','1'),(4,'1','0'),(5,'1','1'),(6,'1','2'),(7,'1','3'),(8,'1','4'),(10,'2','0'),(11,'2','1'),(12,'2','2'),(13,'2','3'),(14,'2','4'),(16,'3','0'),(17,'3','1'),(18,'3','2'),(19,'3','3'),(20,'3','4');
/*!40000 ALTER TABLE `modi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paths`
--

DROP TABLE IF EXISTS `paths`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paths` (
  `id` int(11) NOT NULL DEFAULT '0',
  `computer_id` varchar(45) DEFAULT NULL,
  `user_id` varchar(45) DEFAULT NULL,
  `root` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paths`
--

LOCK TABLES `paths` WRITE;
/*!40000 ALTER TABLE `paths` DISABLE KEYS */;
INSERT INTO `paths` VALUES (0,'0','2','F:\\\\'),(1,'1','1','/home/sungw389/'),(2,'2','1','/sfs/fs5/home-sh/sungw389/'),(3,'3','0','/home/jens/'),(4,'4','2','C:\\\\');
/*!40000 ALTER TABLE `paths` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `preconditioner`
--

DROP TABLE IF EXISTS `preconditioner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `preconditioner` (
  `id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `specification` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `preconditioner`
--

LOCK TABLES `preconditioner` WRITE;
/*!40000 ALTER TABLE `preconditioner` DISABLE KEYS */;
INSERT INTO `preconditioner` VALUES (0,'none','0'),(1,'jacobi','1');
/*!40000 ALTER TABLE `preconditioner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `preconditioner_mkl`
--

DROP TABLE IF EXISTS `preconditioner_mkl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `preconditioner_mkl` (
  `id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `specification` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `preconditioner_mkl`
--

LOCK TABLES `preconditioner_mkl` WRITE;
/*!40000 ALTER TABLE `preconditioner_mkl` DISABLE KEYS */;
INSERT INTO `preconditioner_mkl` VALUES (0,'none','0');
/*!40000 ALTER TABLE `preconditioner_mkl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `preconditioner_petsc`
--

DROP TABLE IF EXISTS `preconditioner_petsc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `preconditioner_petsc` (
  `id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `specification` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `preconditioner_petsc`
--

LOCK TABLES `preconditioner_petsc` WRITE;
/*!40000 ALTER TABLE `preconditioner_petsc` DISABLE KEYS */;
INSERT INTO `preconditioner_petsc` VALUES (0,'none','none'),(1,'jacobi','jacobi'),(2,'bjacobi','bjacobi'),(3,'sor','sor'),(4,'asm','asm'),(5,'mg','mg');
/*!40000 ALTER TABLE `preconditioner_petsc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solver`
--

DROP TABLE IF EXISTS `solver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `solver` (
  `id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `specification` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solver`
--

LOCK TABLES `solver` WRITE;
/*!40000 ALTER TABLE `solver` DISABLE KEYS */;
INSERT INTO `solver` VALUES (1,'gauss','1'),(2,'bcgs','2'),(3,'bicg','3'),(4,'qmrggStab','4'),(5,'cg','5'),(6,'cgnr','6'),(7,'cgs','7'),(8,'richardson','8'),(9,'jor','9'),(10,'sor','10'),(11,'amg1r5','11'),(12,'umf','12'),(13,'gmres','13');
/*!40000 ALTER TABLE `solver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solver_mkl`
--

DROP TABLE IF EXISTS `solver_mkl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `solver_mkl` (
  `id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `specification` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solver_mkl`
--

LOCK TABLES `solver_mkl` WRITE;
/*!40000 ALTER TABLE `solver_mkl` DISABLE KEYS */;
INSERT INTO `solver_mkl` VALUES (0,'pardiso','805');
/*!40000 ALTER TABLE `solver_mkl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solver_petsc`
--

DROP TABLE IF EXISTS `solver_petsc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `solver_petsc` (
  `id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `specification` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solver_petsc`
--

LOCK TABLES `solver_petsc` WRITE;
/*!40000 ALTER TABLE `solver_petsc` DISABLE KEYS */;
INSERT INTO `solver_petsc` VALUES (0,'bcgs','bcgs'),(1,'gmres','gmres');
/*!40000 ALTER TABLE `solver_petsc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `superuser`
--

DROP TABLE IF EXISTS `superuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `superuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `computer_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `superuser`
--

LOCK TABLES `superuser` WRITE;
/*!40000 ALTER TABLE `superuser` DISABLE KEYS */;
INSERT INTO `superuser` VALUES (1,'jens',2,1),(2,'jens',3,0),(3,'jens',4,2),(4,'jens',0,2),(5,'jens',1,1);
/*!40000 ALTER TABLE `superuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `types`
--

DROP TABLE IF EXISTS `types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `types` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(45) DEFAULT NULL,
  `numberOfCPUs` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `types`
--

LOCK TABLES `types` WRITE;
/*!40000 ALTER TABLE `types` DISABLE KEYS */;
INSERT INTO `types` VALUES (0,'2D_plane_xy',2),(1,'2D_plane_xz',2),(2,'3D_box',2),(3,'3D_box_2',2),(4,'axisymmetry_cylinder',2),(5,'1D_analyt',2),(6,'2D_analyt',2),(7,'2D_plume',2),(8,'bc_st_test_hex',2),(9,'bc_st_test_pris',2),(10,'elder',2),(11,'LPVC_1D',2),(12,'LPVC_2D',2),(13,'NNNC_pole',2),(14,'NNNC_poles_O',2),(15,'NNNC_poles_U',2),(16,'anisotropy',2),(17,'kueper',2),(18,'buckleyLeverett',2),(19,'mcWhorter',2),(20,'liakopoulos',2),(21,'TH2M',2),(22,'celia',2),(23,'drainage',2),(24,'plumber',2),(25,'chemistry',2),(26,'NAPL-dissolution',2),(27,'HM',2),(28,'THM',2),(29,'numerics',2);
/*!40000 ALTER TABLE `types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (0,'jens'),(1,'sungw389'),(2,'delfs');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-06-29 15:12:03
