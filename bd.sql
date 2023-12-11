DROP DATABASE IF EXISTS `restaurant`;
CREATE DATABASE IF NOT EXISTS `restaurant` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `restaurant`;

DROP TABLE IF EXISTS `comandes`;
CREATE TABLE IF NOT EXISTS `comandes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `producte` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `quantitat` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`,`producte`) USING BTREE,
  KEY `FK_comanda_productes` (`producte`),
  CONSTRAINT `FK_comanda_productes` FOREIGN KEY (`producte`) REFERENCES `productes` (`nom`) ON UPDATE CASCADE,
  CONSTRAINT `FK_comandes_registres` FOREIGN KEY (`id`) REFERENCES `registres` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DELETE FROM `comandes`;
INSERT INTO `comandes` (`id`, `producte`, `quantitat`) VALUES
	(1, 'aigua de jamaica', 2),
	(1, 'crema catalana', 1),
	(2, 'cafè amb llet', 1),
	(2, 'gin tonic amb gerds i llimona', 3),
	(2, 'picapoll negre', 5),
	(2, 'tallat', 1),
	(3, 'profiteroles farcits de crema', 1);

DROP TABLE IF EXISTS `productes`;
CREATE TABLE IF NOT EXISTS `productes` (
  `nom` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `preu` float DEFAULT NULL,
  `tipus` enum('entrant','1r plat','2n plat','postre','beguda','cafè i petit fours','acompanyaments') CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `imatge` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`nom`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DELETE FROM `productes`;
INSERT INTO `productes` (`nom`, `preu`, `tipus`, `stock`, `imatge`) VALUES
	('aigua de coco natural', 2.5, 'beguda', 100, './img/plats/aigua de coco natural.jpeg'),
	('aigua de jamaica', 4, 'beguda', 100, './img/plats/aigua de jamaica.jpeg'),
	('amanida d\'espinacs amb maduixes i nous', 8, 'acompanyaments', 50, './img/plats/amanida espinacs amb maduixes i nous.jpeg'),
	('amanida de quinoa amb alvocat i tomàquet', 8, 'entrant', 50, './img/plats/amanida de quinoa amb alvocat i tomaquet.jpeg'),
	('arròs integral amb ametlles torrades', 7, 'acompanyaments', 50, './img/plats/arros integral amb ametlles torrades.jpeg'),
	('bonaigua amb gas', 2.5, 'beguda', 100, './img/plats/bonaigua amb gas.jpeg'),
	('broquetes de vedella amb verdures a la graella', 13, '2n plat', 50, './img/plats/broquetes de vedella amb verdures a la graella.jpeg'),
	('bruschetta de tomàquet i alvàcada', 9, '1r plat', 50, './img/plats/bruschetta de tomaquet i alvacada.jpeg'),
	('cafè', 2, 'cafè i petit fours', 500, './img/plats/cafe.jpeg'),
	('cafè amb llet', 2.5, 'cafè i petit fours', 500, './img/plats/cafe amb llet.jpeg'),
	('caipirinha de mango', 8.5, 'beguda', 100, './img/plats/caipirinha de mango.jpeg'),
	('cervesa de blat amb tangerina', 4.5, 'beguda', 100, './img/plats/cervesa de blat amb tangerina.jpeg'),
	('cervesa lager refrescant', 3.5, 'beguda', 100, './img/plats/cervesa lager refrescant.jpeg'),
	('cervesa negra artesana', 5, 'beguda', 100, './img/plats/cervesa negra artesana.jpeg'),
	('ceviche de peix amb mango', 13, '1r plat', 50, './img/plats/ceviche de peix amb mango.jpeg'),
	('cheesecake de fruits vermells', 10, 'postre', 50, './img/plats/cheesecake de fruits vermells.jpeg'),
	('coca-cola', 3, 'beguda', 500, './img/plats/coca-cola.jpeg'),
	('crema catalana', 9, 'postre', 50, './img/plats/crema catalana.jpeg'),
	('espàrrecs a la graella amb allioli', 9, 'acompanyaments', 50, './img/plats/esparrecs a la graella amb allioli.png'),
	('faletes d\'avena i panses', 4, 'cafè i petit fours', 50, './img/plats/faletes avena i panses.jpeg'),
	('fanta llimona', 3, 'beguda', 500, './img/plats/fanta llimona.jpeg'),
	('fanta tronja', 3, 'beguda', 500, './img/plats/fanta tronja.jpeg'),
	('filet de salmó al forn amb costra d\'herbes', 15, '2n plat', 50, './img/plats/filet de salmo al forn amb costra herbes.jpeg'),
	('fondue de xocolata amb fruita', 10, 'postre', 50, './img/plats/fondue de xocolata amb fruita.jpeg'),
	('freixenet', 18, 'beguda', 100, './img/plats/freixenet.jpeg'),
	('fruites fresques amb crema de mascarpone', 7, 'postre', 50, './img/plats/fruites fresques amb crema de mascarpone.jpeg'),
	('gazpacho andalús', 7, 'entrant', 50, './img/plats/gazpacho andalus.jpeg'),
	('gelat de vainilla amb salsa de caramel ', 6, 'postre', 50, './img/plats/gelat de vainilla amb salsa de caramel.jpeg'),
	('gin tonic amb gerds i llimona', 10, 'beguda', 100, './img/plats/gin tonic amb gerds i llimona.jpeg'),
	('hummus amb bastonets de pastanaga i cogombre', 6, 'entrant', 50, './img/plats/hummus amb bastonets de pastanaga i cogombre.jpeg'),
	('llasanya d\'albergínia i ricotta', 11, '2n plat', 50, './img/plats/llasanya alberginia i ricotta.jpeg'),
	('llimonada de menta', 5, 'beguda', 100, './img/plats/llimonada de menta.jpeg'),
	('llimonada fresca', 3, 'beguda', 100, './img/plats/llimonada fresca.jpeg'),
	('macarons variats', 8, 'cafè i petit fours', 50, './img/plats/macarons variats.jpeg'),
	('margarita de maduixa', 7.5, 'beguda', 100, './img/plats/margarita de maduixa.jpeg'),
	('mini croissants farcits de xocolata', 5, 'cafè i petit fours', 50, './img/plats/mini croissants farcits de xocolata.jpeg'),
	('mini tartaletes de fruita', 6, 'cafè i petit fours', 50, './img/plats/mini tartaletes de fruita.jpeg'),
	('mojito clàssic', 8, 'beguda', 100, './img/plats/mojito classic.jpeg'),
	('mojito de maduixa', 8, 'beguda', 100, './img/plats/mojito de maduixa.jpeg'),
	('mousse de xocolata', 9, 'postre', 50, './img/plats/mousse de xocolata.jpeg'),
	('natilles amb galetes', 6, 'postre', 50, './img/plats/natilles amb galetes.jpeg'),
	('pastís de poma amb gelat de canyella', 8, 'postre', 50, './img/plats/pastis de poma amb gelat de canyella.jpeg'),
	('patates braves amb salsa brava i allioli', 7, 'acompanyaments', 50, './img/plats/patates braves amb salsa brava i allioli.jpeg'),
	('picapoll negre', 20, 'beguda', 100, './img/plats/picapoll negre.jpeg'),
	('pinya colada', 9, 'beguda', 100, './img/plats/pinya colada.jpeg'),
	('pollastre a la graella amb salsa de llimona i herbes', 14, '2n plat', 50, './img/plats/pollastre a la graella amb salsa de llimona i herbes.jpeg'),
	('profiteroles farcits de crema', 7, 'postre', 50, './img/plats/profiteroles farcits de crema.jpeg'),
	('puré de patates amb all i parmesà', 6, 'acompanyaments', 50, './img/plats/pure de patates amb all i parmesa.jpeg'),
	('risotto de xampinyons i parmesà', 12, '1r plat', 50, './img/plats/risotto de xampinyons i parmesa.jpeg'),
	('rotllets de primavera amb salsa agredolça', 10, 'entrant', 50, './img/plats/rotllets de primavera amb salsa agredolca.jpeg'),
	('sangria de fruites', 10, 'beguda', 100, './img/plats/sangria de fruites.jpeg'),
	('sopa de llenties amb xoriço', 8, '1r plat', 50, './img/plats/sopa de llenties amb xorico.jpeg'),
	('spaghetti carbonara', 11, '1r plat', 50, './img/plats/spaghetti carbonara.jpeg'),
	('suc de taronja natural', 3.5, 'beguda', 100, './img/plats/suc de taronja natural.jpeg'),
	('tacos de carn amb salsa d\'alvocat', 12, '2n plat', 50, './img/plats/tacos de carn amb salsa alvocat.jpeg'),
	('tallat', 2, 'cafè i petit fours', 50, './img/plats/tallat.jpeg'),
	('tiramisú', 8, 'postre', 50, './img/plats/tiramisu.jpeg'),
	('torrades d\'alvocat amb ou pocat', 9, 'entrant', 50, './img/plats/torrades alvocat amb ou pocat.jpeg'),
	('trufes de xocolata', 7, 'cafè i petit fours', 50, './img/plats/trufes de xocolata.jpeg'),
	('xocolata calenta amb malvaviscos', 4, 'postre', 50, './img/plats/xocolata calenta amb malvaviscos.jpeg');

DROP TABLE IF EXISTS `registres`;
CREATE TABLE IF NOT EXISTS `registres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_taula` int(11) NOT NULL,
  `data` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT=' ';

DELETE FROM `registres`;
INSERT INTO `registres` (`id`, `id_taula`, `data`) VALUES
	(1, 1, '2023-11-28'),
	(2, 1, '2023-11-28'),
	(3, 14, '2023-11-30');