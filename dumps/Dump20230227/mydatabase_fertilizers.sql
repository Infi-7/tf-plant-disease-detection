-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mydatabase
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `fertilizers`
--

DROP TABLE IF EXISTS `fertilizers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fertilizers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `crop` varchar(255) DEFAULT NULL,
  `disease` varchar(255) DEFAULT NULL,
  `remedy` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fertilizers`
--

LOCK TABLES `fertilizers` WRITE;
/*!40000 ALTER TABLE `fertilizers` DISABLE KEYS */;
INSERT INTO `fertilizers` VALUES (1,'Pepper bell','Bacterial spot','Coppera + Mancozeb'),(2,'Pepper bell','Bacterial spot','Tanos® + copper alternated with copper + Mancozeb'),(3,'Pepper bell','Bacterial spot','Serenade® ASO + Badge® X2 copper'),(4,'Potato','Early blight','Quadris'),(5,'Potato','Early blight','BOSCALID'),(6,'Potato','Early blight','CHLOROTHALONIL'),(7,'Potato','Late blight','tanos fungicide'),(8,'Potato','Late blight','Curzate 60 DF'),(9,'Potato','Late blight','DIMETHOMORPH fungicide'),(10,'Tomato','Bacterial spot','Kocide 3000'),(11,'Tomato','Bacterial spot','Dithane M-45'),(12,'Tomato','Bacterial spot','Penncozeb 75DF'),(13,'Tomato','Early blight','BONIDE® Copper Fungicide Dust'),(14,'Tomato','Early blight','ECOMONAS'),(15,'Tomato','Early blight','Multiplex Biojodi'),(16,'Tomato','Late blight','Zampro'),(17,'Tomato','Late blight','Quadris Top'),(18,'Tomato','Late blight','Bravo Weather Stik'),(19,'Tomato','Leaf Mold','Champ 30 WG'),(20,'Tomato','Leaf Mold','zonix fungicide'),(21,'Tomato','Septoria leaf spot','maneb'),(22,'Tomato','Septoria leaf spot','mancozeb'),(23,'Tomato','Septoria leaf spot','chlorothalonil'),(24,'Tomato','Spider mites Two spotted spider mite','Nuke Em'),(25,'Tomato','Spider mites Two spotted spider mite','BotaniGard ES'),(26,'Tomato','Spider mites Two spotted spider mite','Fosmite'),(27,'Tomato','Target Spot','azoxystrobin'),(28,'Tomato','Target Spot','Mulch '),(29,'Tomato','YellowLeaf Curl Virus','dinotefuran'),(30,'Tomato','YellowLeaf Curl Virus','imidacloprid'),(31,'Tomato','YellowLeaf Curl Virus','thiamethoxam'),(32,'Tomato','mosaic virus','Safer Soap'),(33,'Tomato','mosaic virus','Bon-Neem'),(34,'Tomato','mosaic virus','Diatomaceous Earth');
/*!40000 ALTER TABLE `fertilizers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-27 17:08:06
