CREATE DATABASE IF NOT EXISTS `cafepro` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `cafepro`;

CREATE TABLE `cafeuser` (
  `QrNum` varchar(20) NOT NULL,
  `FName` varchar(20) NOT NULL,
  `MName` varchar(20) NOT NULL,
  `LName` varchar(20) NOT NULL,
  `userMonth` int(11) NOT NULL,
  `userDate` int(11) NOT NULL,
  `Breakfast` int(11) NOT NULL,
  `Lunch` int(11) NOT NULL,
  `Dinner` int(11) NOT NULL,
  `Disabled` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


INSERT INTO `cafeuser` (`QrNum`, `FName`, `MName`, `LName`, `userMonth`, `userDate`, `Breakfast`, `Lunch`, `Dinner`, `Disabled`) VALUES
('1622', 'Habib', 'Endris', 'Mohammed', 1, 26, 1, 0, 0, 0),
('1162', 'Elyas', 'Abate', 'Amare', 1, 26, 0, 0, 0, 0);


CREATE TABLE `cheateruser` (
  `QrNum` varchar(20) NOT NULL,
  `userMonth` int(11) NOT NULL,
  `userDate` int(11) NOT NULL,
  `ImageName` varchar(1000) NOT NULL,
  `Breakfast` int(11) NOT NULL,
  `Lunch` int(11) NOT NULL,
  `Dinner` int(11) NOT NULL,
  `Tried` int(11) NOT NULL,
  `OtherMeal` int(11) NOT NULL,
  `Disabled` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `cheateruser` (`QrNum`, `userMonth`, `userDate`, `ImageName`, `Breakfast`, `Lunch`, `Dinner`, `Tried`, `OtherMeal`, `Disabled`) VALUES
('1622', 1, 26, '20181261', 1, 0, 0, 1, 0, 0),
('1622', 1, 26, '20181262', 1, 0, 0, 1, 0, 0),
('1622', 1, 26, '20181263', 1, 0, 0, 1, 0, 0),
('1622', 1, 26, '20181264', 1, 0, 0, 0, 1, 0);

CREATE TABLE `mealtime` (
  `mealMonth` int(11) NOT NULL,
  `mealDate` int(11) NOT NULL,
  `Breakfast` int(11) NOT NULL,
  `Lunch` int(11) NOT NULL,
  `Dinner` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
