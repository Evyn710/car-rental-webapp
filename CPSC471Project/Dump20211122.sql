-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: rentalcompany
-- ------------------------------------------------------
-- Server version	8.0.23

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
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account` (
  `Username` varchar(20) NOT NULL,
  `Password` varchar(60) NOT NULL,
  PRIMARY KEY (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES ('Agent1','$2b$12$FqxzPfw3KiYz7XvXqvbiduJ4l5mJsIUP06e.MoEEwpQQr6aW2lthm'),('Agent2','$2b$12$QgjypUMAMTli.kR4ANYGN.3ob6gFDV53RwOA0b.TdnFBLNOkN9lMK'),('Employee','$2b$12$UzqVmPZewq3hMOQ1xSQmleZ4oEwtxRPXcFFLr5E6NhIRKpoihNpW2'),('EvynRissling','$2b$12$JwZHuzrafuIuaGzV8XpLpuev.ibeSAGmzvn7T2hQ/gs3ifVDOjjzG'),('JohnA','$2b$12$kt503l2Ivi8BQ0WcsxjxseXh.Xa7UgxdFJTztiaJ/bPooXsRBDYDm'),('JonMulyk','$2b$12$8Lsy3U7N9N8yu8HmmYYsTu4P2//ZGVl95GDLOJgJrJ2CmaxkyKpE2'),('Manager','$2b$12$F.um9f6F6WwKDWsGrP9Vauw07mW3coVBF1LIvmymjszr.JanwV1V6'),('Mechanic','$2b$12$jXSaPpKKc8LT.m4IOnSB2O3hT0.t5lbqmw4qkQBUOa9XSNl1Ydm.W'),('TestAPI','$2b$12$fKVyzuWRD5zXqFdB77QbGutj86yl9qVCg3lColmtbMSSJiBKuk0xC');
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `agent`
--

DROP TABLE IF EXISTS `agent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agent` (
  `Agent_SSN` int NOT NULL,
  PRIMARY KEY (`Agent_SSN`),
  CONSTRAINT `SSN` FOREIGN KEY (`Agent_SSN`) REFERENCES `employee` (`SSN`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agent`
--

LOCK TABLES `agent` WRITE;
/*!40000 ALTER TABLE `agent` DISABLE KEYS */;
INSERT INTO `agent` VALUES (3),(4);
/*!40000 ALTER TABLE `agent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `airport`
--

DROP TABLE IF EXISTS `airport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `airport` (
  `Name` varchar(45) NOT NULL,
  `City` varchar(45) NOT NULL,
  `Address` varchar(45) NOT NULL,
  PRIMARY KEY (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `airport`
--

LOCK TABLES `airport` WRITE;
/*!40000 ALTER TABLE `airport` DISABLE KEYS */;
INSERT INTO `airport` VALUES ('Calgary International Airport','Calgary','2000 Airport Rd NE');
/*!40000 ALTER TABLE `airport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Username` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `Username_UNIQUE` (`Username`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (2,'Evyn Rissling','EvynRissling'),(3,'John Abo','JohnA'),(4,'Jon Mulyk','JonMulyk'),(5,'Mr. Manager','Manager'),(6,'Mrs. Employee','Employee'),(7,'Mr. Agent','Agent1'),(8,'Mrs. Agent','Agent2'),(9,'Mrs. Mechanic','Mechanic');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `SSN` int NOT NULL,
  `Name` varchar(45) NOT NULL,
  `DOB` varchar(45) NOT NULL,
  `Sex` char(1) NOT NULL,
  `Salary` int NOT NULL,
  `Username` varchar(20) NOT NULL,
  `City` varchar(45) NOT NULL,
  `Address` varchar(45) NOT NULL,
  `Hours` int DEFAULT NULL,
  `Mgr_ssn` int DEFAULT NULL,
  PRIMARY KEY (`SSN`),
  UNIQUE KEY `SSN_UNIQUE` (`SSN`),
  UNIQUE KEY `Username_UNIQUE` (`Username`),
  KEY `Mgr_ssn_idx` (`Mgr_ssn`),
  CONSTRAINT `Mgr_ssn` FOREIGN KEY (`Mgr_ssn`) REFERENCES `employee` (`SSN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'Mr. Manager','1992-05-09','M',78000,'Manager','Airdrie','1293 Bridgeland Street',52,NULL),(2,'Evyn Rissling','2001-07-10','M',73245,'EvynRissling','Airdrie','1293 Bridgeland Street',40,1),(3,'Mr. Agent','1992-05-09','M',65780,'Agent1','Calgary','9812 University Drive',23,1),(4,'Mrs. Agent','1992-05-09','F',74623,'Agent2','Calgary','9812 University Drive',45,1),(5,'Mrs. Mechanic','1992-05-09','F',57968,'Mechanic','Airdrie','1293 Bridgeland Street',12,1),(6,'Mrs. Employee','1992-05-09','F',61245,'Employee','Calgary','9812 University Drive',32,1);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `garage`
--

DROP TABLE IF EXISTS `garage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `garage` (
  `GarageNo` int NOT NULL AUTO_INCREMENT,
  `City` varchar(45) NOT NULL,
  `Address` varchar(45) NOT NULL,
  `Capacity` int DEFAULT NULL,
  PRIMARY KEY (`GarageNo`),
  KEY `garage_location_idx` (`City`,`Address`),
  CONSTRAINT `garage_location` FOREIGN KEY (`City`, `Address`) REFERENCES `location` (`City`, `Address`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `garage`
--

LOCK TABLES `garage` WRITE;
/*!40000 ALTER TABLE `garage` DISABLE KEYS */;
INSERT INTO `garage` VALUES (1,'Airdrie','1293 Bridgeland Street',12),(2,'Airdrie','1293 Bridgeland Street',15),(4,'Calgary','9812 University Drive',20);
/*!40000 ALTER TABLE `garage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `garage_shuttle`
--

DROP TABLE IF EXISTS `garage_shuttle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `garage_shuttle` (
  `Shuttle_no` int NOT NULL AUTO_INCREMENT,
  `City` varchar(45) NOT NULL,
  `Address` varchar(45) NOT NULL,
  `GarageNo` int NOT NULL,
  PRIMARY KEY (`Shuttle_no`),
  KEY `garage_shuttle_location_idx` (`City`,`Address`),
  KEY `garage_shuttle_garage#_idx` (`GarageNo`),
  CONSTRAINT `garage_shuttle_garage#` FOREIGN KEY (`GarageNo`) REFERENCES `garage` (`GarageNo`),
  CONSTRAINT `garage_shuttle_location` FOREIGN KEY (`City`, `Address`) REFERENCES `location` (`City`, `Address`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `garage_shuttle`
--

LOCK TABLES `garage_shuttle` WRITE;
/*!40000 ALTER TABLE `garage_shuttle` DISABLE KEYS */;
INSERT INTO `garage_shuttle` VALUES (1,'Calgary','9812 University Drive',4),(2,'Calgary','9812 University Drive',4),(3,'Calgary','9812 University Drive',4),(4,'Calgary','9812 University Drive',4),(5,'Airdrie','1293 Bridgeland Street',1),(7,'Airdrie','1293 Bridgeland Street',2),(12,'Calgary','9812 University Drive',4);
/*!40000 ALTER TABLE `garage_shuttle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insurance_plan`
--

DROP TABLE IF EXISTS `insurance_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insurance_plan` (
  `PlanNo` int NOT NULL AUTO_INCREMENT,
  `Price` double NOT NULL,
  `Coverage` varchar(45) NOT NULL,
  PRIMARY KEY (`PlanNo`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insurance_plan`
--

LOCK TABLES `insurance_plan` WRITE;
/*!40000 ALTER TABLE `insurance_plan` DISABLE KEYS */;
INSERT INTO `insurance_plan` VALUES (27,75,'partial'),(28,45,'full'),(29,40,'full');
/*!40000 ALTER TABLE `insurance_plan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insurance_transaction`
--

DROP TABLE IF EXISTS `insurance_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insurance_transaction` (
  `Customer_id` int NOT NULL,
  `PlanNo` int NOT NULL,
  `Agent_SSN` int DEFAULT NULL,
  PRIMARY KEY (`Customer_id`,`PlanNo`),
  KEY `insurance_trans_plan#_idx` (`PlanNo`),
  KEY `insurance_trans_agent_ssn_idx` (`Agent_SSN`),
  CONSTRAINT `insurance_trans_agent_ssn` FOREIGN KEY (`Agent_SSN`) REFERENCES `agent` (`Agent_SSN`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `insurance_trans_cust_id` FOREIGN KEY (`Customer_id`) REFERENCES `customer` (`ID`),
  CONSTRAINT `insurance_trans_plan#` FOREIGN KEY (`PlanNo`) REFERENCES `insurance_plan` (`PlanNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insurance_transaction`
--

LOCK TABLES `insurance_transaction` WRITE;
/*!40000 ALTER TABLE `insurance_transaction` DISABLE KEYS */;
INSERT INTO `insurance_transaction` VALUES (2,28,4),(3,27,4),(3,29,4);
/*!40000 ALTER TABLE `insurance_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `location` (
  `City` varchar(45) NOT NULL,
  `Address` varchar(45) NOT NULL,
  `Mgr_ssn` int NOT NULL,
  PRIMARY KEY (`City`,`Address`),
  KEY `manager_idx` (`Mgr_ssn`),
  CONSTRAINT `manager` FOREIGN KEY (`Mgr_ssn`) REFERENCES `employee` (`Mgr_ssn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location`
--

LOCK TABLES `location` WRITE;
/*!40000 ALTER TABLE `location` DISABLE KEYS */;
INSERT INTO `location` VALUES ('Airdrie','1293 Bridgeland Street',12345),('Calgary','9812 University Drive',12345);
/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mechanic`
--

DROP TABLE IF EXISTS `mechanic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mechanic` (
  `Mechanic_SSN` int NOT NULL,
  PRIMARY KEY (`Mechanic_SSN`),
  CONSTRAINT `MechSSN` FOREIGN KEY (`Mechanic_SSN`) REFERENCES `employee` (`SSN`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mechanic`
--

LOCK TABLES `mechanic` WRITE;
/*!40000 ALTER TABLE `mechanic` DISABLE KEYS */;
INSERT INTO `mechanic` VALUES (5);
/*!40000 ALTER TABLE `mechanic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rental`
--

DROP TABLE IF EXISTS `rental`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rental` (
  `RegNo` int NOT NULL AUTO_INCREMENT,
  `Color` varchar(10) NOT NULL,
  `Status` varchar(15) NOT NULL,
  `Make` varchar(20) NOT NULL,
  `Model` varchar(20) NOT NULL,
  `City` varchar(20) NOT NULL,
  `Address` varchar(40) NOT NULL,
  `Price` double NOT NULL,
  PRIMARY KEY (`RegNo`),
  KEY `location_idx` (`City`,`Address`),
  KEY `rental_location_idx` (`City`,`Address`),
  CONSTRAINT `rental_location` FOREIGN KEY (`City`, `Address`) REFERENCES `location` (`City`, `Address`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rental`
--

LOCK TABLES `rental` WRITE;
/*!40000 ALTER TABLE `rental` DISABLE KEYS */;
INSERT INTO `rental` VALUES (13,'Red','available','Ford','Mustang','Airdrie','1293 Bridgeland Street',300),(14,'Blue','available','Dodge','Grand Caravan','Calgary','9812 University Drive',225),(15,'Red','rented','Ford','Escape','Airdrie','1293 Bridgeland Street',225),(16,'Blue','rented','Dodge','Dart','Calgary','9812 University Drive',150),(17,'Black','rented','Dodge','Durango','Airdrie','1293 Bridgeland Street',225),(18,'Red','available','Kia','Soul','Airdrie','1293 Bridgeland Street',200),(20,'Orange','serviced','Dodge','Calibre','Calgary','9812 University Drive',175),(21,'Yellow','rented','Dodge','Viper','Calgary','9812 University Drive',500),(22,'Silver','available','Hyundai','Santa Fe','Calgary','9812 University Drive',225),(24,'Black','available','Honda','Accord','Calgary','9812 University Drive',150);
/*!40000 ALTER TABLE `rental` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rental_return`
--

DROP TABLE IF EXISTS `rental_return`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rental_return` (
  `Customer_id` int NOT NULL,
  `RegNo` int NOT NULL,
  `City` varchar(45) NOT NULL,
  `Address` varchar(45) NOT NULL,
  `Date` date NOT NULL,
  `Time` time NOT NULL,
  PRIMARY KEY (`Customer_id`),
  KEY `return_reg#_idx` (`RegNo`),
  KEY `return_location_idx` (`City`,`Address`),
  CONSTRAINT `return_customer_id` FOREIGN KEY (`Customer_id`) REFERENCES `customer` (`ID`),
  CONSTRAINT `return_location` FOREIGN KEY (`City`, `Address`) REFERENCES `location` (`City`, `Address`),
  CONSTRAINT `return_reg#` FOREIGN KEY (`RegNo`) REFERENCES `rental` (`RegNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rental_return`
--

LOCK TABLES `rental_return` WRITE;
/*!40000 ALTER TABLE `rental_return` DISABLE KEYS */;
INSERT INTO `rental_return` VALUES (3,18,'Airdrie','1293 Bridgeland Street','2021-12-17','12:32:47');
/*!40000 ALTER TABLE `rental_return` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rental_service`
--

DROP TABLE IF EXISTS `rental_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rental_service` (
  `Mechanic_SSN` int NOT NULL,
  `RegNo` int NOT NULL,
  `Date` date NOT NULL,
  `Hours` int NOT NULL,
  PRIMARY KEY (`Mechanic_SSN`),
  KEY `rental_service_rental#_idx` (`RegNo`),
  CONSTRAINT `rental_service_mgr_ssn` FOREIGN KEY (`Mechanic_SSN`) REFERENCES `mechanic` (`Mechanic_SSN`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `rental_service_rental#` FOREIGN KEY (`RegNo`) REFERENCES `rental` (`RegNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rental_service`
--

LOCK TABLES `rental_service` WRITE;
/*!40000 ALTER TABLE `rental_service` DISABLE KEYS */;
INSERT INTO `rental_service` VALUES (5,20,'2021-12-17',2);
/*!40000 ALTER TABLE `rental_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rents`
--

DROP TABLE IF EXISTS `rents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rents` (
  `Customer_id` int NOT NULL,
  `RegNo` int NOT NULL,
  `Price` double NOT NULL,
  `Start_date` date NOT NULL,
  `End_date` date NOT NULL,
  PRIMARY KEY (`Customer_id`,`RegNo`),
  KEY `Rents_reg#_idx` (`RegNo`),
  CONSTRAINT `Customer_id` FOREIGN KEY (`Customer_id`) REFERENCES `customer` (`ID`),
  CONSTRAINT `Rents_reg#` FOREIGN KEY (`RegNo`) REFERENCES `rental` (`RegNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rents`
--

LOCK TABLES `rents` WRITE;
/*!40000 ALTER TABLE `rents` DISABLE KEYS */;
INSERT INTO `rents` VALUES (2,17,450,'2021-12-16','2021-12-18'),(3,18,400,'2021-12-16','2021-12-18'),(3,21,1500,'2021-12-16','2021-12-19');
/*!40000 ALTER TABLE `rents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shuttle`
--

DROP TABLE IF EXISTS `shuttle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shuttle` (
  `Number` int NOT NULL AUTO_INCREMENT,
  `Capacity` int NOT NULL,
  `Airport_name` varchar(45) DEFAULT NULL,
  `Schedule` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Number`),
  UNIQUE KEY `Number_UNIQUE` (`Number`),
  KEY `airport_name_idx` (`Airport_name`),
  CONSTRAINT `airport_name` FOREIGN KEY (`Airport_name`) REFERENCES `airport` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shuttle`
--

LOCK TABLES `shuttle` WRITE;
/*!40000 ALTER TABLE `shuttle` DISABLE KEYS */;
INSERT INTO `shuttle` VALUES (1,12,'Calgary International Airport','MWF'),(2,13,'Calgary International Airport','TThF'),(3,32,'Calgary International Airport','F'),(4,13,'Calgary International Airport','SSu'),(5,21,'Calgary International Airport','SSu'),(7,19,'Calgary International Airport','MWTThF'),(12,22,NULL,NULL);
/*!40000 ALTER TABLE `shuttle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shuttle_service`
--

DROP TABLE IF EXISTS `shuttle_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shuttle_service` (
  `Mechanic_SSN` int NOT NULL,
  `ShuttleNo` int NOT NULL,
  `Date` date NOT NULL,
  `Hours` int NOT NULL,
  PRIMARY KEY (`Mechanic_SSN`),
  KEY `shuttle_service_shuttle#_idx` (`ShuttleNo`),
  KEY `shuttle_service#_idx` (`ShuttleNo`),
  CONSTRAINT `shuttle_service#` FOREIGN KEY (`ShuttleNo`) REFERENCES `shuttle` (`Number`),
  CONSTRAINT `shuttle_service_mech_ssn` FOREIGN KEY (`Mechanic_SSN`) REFERENCES `mechanic` (`Mechanic_SSN`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shuttle_service`
--

LOCK TABLES `shuttle_service` WRITE;
/*!40000 ALTER TABLE `shuttle_service` DISABLE KEYS */;
INSERT INTO `shuttle_service` VALUES (5,4,'2021-12-16',5);
/*!40000 ALTER TABLE `shuttle_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `works_in`
--

DROP TABLE IF EXISTS `works_in`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `works_in` (
  `Mechanic_SSN` int NOT NULL,
  `City` varchar(45) NOT NULL,
  `Address` varchar(45) NOT NULL,
  `GarageNo` int NOT NULL,
  `Hours` int NOT NULL,
  PRIMARY KEY (`Mechanic_SSN`,`City`,`Address`,`GarageNo`),
  KEY `works_in_location_idx` (`City`,`Address`),
  KEY `works_in_garage#_idx` (`GarageNo`),
  CONSTRAINT `works_in_garage#` FOREIGN KEY (`GarageNo`) REFERENCES `garage` (`GarageNo`),
  CONSTRAINT `works_in_location` FOREIGN KEY (`City`, `Address`) REFERENCES `location` (`City`, `Address`),
  CONSTRAINT `works_in_mech_SSN` FOREIGN KEY (`Mechanic_SSN`) REFERENCES `mechanic` (`Mechanic_SSN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `works_in`
--

LOCK TABLES `works_in` WRITE;
/*!40000 ALTER TABLE `works_in` DISABLE KEYS */;
INSERT INTO `works_in` VALUES (5,'Airdrie','1293 Bridgeland Street',1,4),(5,'Airdrie','1293 Bridgeland Street',2,5);
/*!40000 ALTER TABLE `works_in` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-17 14:47:10
