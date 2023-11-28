/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `restaurant` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `restaurant`;

CREATE TABLE IF NOT EXISTS `comandes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `producte` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `quantitat` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_comanda_productes` (`producte`),
  CONSTRAINT `FK_comanda_productes` FOREIGN KEY (`producte`) REFERENCES `productes` (`nom`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DELETE FROM `comandes`;

CREATE TABLE IF NOT EXISTS `productes` (
  `nom` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `preu` float DEFAULT NULL,
  `tipus` enum('entrant','1rplat','2nplat','postre','beguda','cafè i petit fours','acompanyaments') CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `imatge` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`nom`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DELETE FROM `productes`;
INSERT INTO `productes` (`nom`, `preu`, `tipus`, `stock`, `imatge`) VALUES
	('aigua de coco natural', 2.5, 'beguda', 100, NULL),
	('aigua de jamaica', 4, 'beguda', 100, NULL),
	('amanida d\'espinacs amb maduixes i nous', 8, 'acompanyaments', 50, NULL),
	('amanida de quinoa amb alvocat i tomàquet', 8, 'entrant', 50, NULL),
	('arròs integral amb ametlles torrades', 7, 'acompanyaments', 50, NULL),
	('bonaigua amb gas', 2.5, 'beguda', 100, NULL),
	('broquetes de vedella amb verdures a la graella', 13, '2nplat', 50, NULL),
	('bruschetta de tomàquet i alvàcada', 9, '1rplat', 50, NULL),
	('cafè ', 2, 'cafè i petit fours', 500, NULL),
	('cafè amb llet', 2.5, 'cafè i petit fours', 500, NULL),
	('caipirinha de mango', 8.5, 'beguda', 100, NULL),
	('cervesa de blat amb tangerina', 4.5, 'beguda', 100, NULL),
	('cervesa lager refrescant', 3.5, 'beguda', 100, NULL),
	('cervesa negra artesana', 5, 'beguda', 100, NULL),
	('ceviche de peix amb mango', 13, '1rplat', 50, NULL),
	('cheesecake de fruits vermells', 10, 'postre', 50, NULL),
	('coca-cola', 3, 'beguda', 500, NULL),
	('crema catalana', 9, 'postre', 50, NULL),
	('espàrrecs a la graella amb allioli', 9, 'acompanyaments', 50, NULL),
	('faletes d\'avena i panses', 4, 'cafè i petit fours', 50, NULL),
	('fanta llimona', 3, 'beguda', 500, NULL),
	('fanta tronja', 3, 'beguda', 500, NULL),
	('filet de salmó al forn amb costra d\'herbes', 15, '2nplat', 50, NULL),
	('fondue de xocolata amb fruita', 10, 'postre', 50, NULL),
	('freixenet', 18, 'beguda', 100, NULL),
	('fruites fresques amb crema de mascarpone', 7, 'postre', 50, NULL),
	('gazpacho andalús', 7, 'entrant', 50, NULL),
	('gelat de vainilla amb salsa de caramel ', 6, 'postre', 50, NULL),
	('gin tonic amb gerds i llimona', 10, 'beguda', 100, NULL),
	('hummus amb bastonets de pastanaga i cogombre', 6, 'entrant', 50, NULL),
	('llasanya d\'albergínia i ricotta', 11, '2nplat', 50, NULL),
	('llimonada de menta', 5, 'beguda', 100, NULL),
	('llimonada fresca', 3, 'beguda', 100, NULL),
	('macarons variats', 8, 'cafè i petit fours', 50, NULL),
	('margarita de maduixa', 7.5, 'beguda', 100, NULL),
	('mini croissants farcits de xocolata', 5, 'cafè i petit fours', 50, NULL),
	('mini tartaletes de fruita', 6, 'cafè i petit fours', 50, NULL),
	('mojito clàssic', 8, 'beguda', 100, NULL),
	('mojito de maduixa', 8, 'beguda', 100, NULL),
	('mousse de xocolata', 9, 'postre', 50, NULL),
	('natilles amb galete', 6, 'postre', 50, NULL),
	('pastís de poma amb gelat de canyella', 8, 'postre', 50, NULL),
	('patates braves amb salsa brava i allioli', 7, 'acompanyaments', 50, NULL),
	('picapoll negre', 20, 'beguda', 100, NULL),
	('pinya colada', 9, 'beguda', 100, NULL),
	('pollastre a la graella amb salsa de llimona i herbes', 14, '2nplat', 50, NULL),
	('profiteroles farcits de crema', 7, 'postre', 50, NULL),
	('puré de patates amb all i parmesà', 6, 'acompanyaments', 50, NULL),
	('risotto de xampinyons i parmesà', 12, '1rplat', 50, NULL),
	('rotllets de primavera amb salsa agredolça', 10, 'entrant', 50, NULL),
	('sangria de fruites', 10, 'beguda', 100, NULL),
	('sopa de llenties amb xoriço', 8, '1rplat', 50, NULL),
	('spaghetti carbonara', 11, '1rplat', 50, NULL),
	('suc de taronja natural', 3.5, 'beguda', 100, NULL),
	('tacos de carn amb salsa d\'alvocat', 12, '2nplat', 50, NULL),
	('tallat', 2, 'cafè i petit fours', 50, NULL),
	('tiramisú', 8, 'postre', 50, NULL),
	('torrades d\'alvocat amb ou pocat', 9, 'entrant', 50, NULL),
	('trufes de xocolata', 7, 'cafè i petit fours', 50, NULL),
	('xocolata calenta amb malvaviscos', 4, 'postre', 50, NULL);

CREATE TABLE IF NOT EXISTS `registre` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_taula` int(11) NOT NULL,
  `data` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `FK__comanda` FOREIGN KEY (`id`) REFERENCES `comandes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT=' ';

DELETE FROM `registre`;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
