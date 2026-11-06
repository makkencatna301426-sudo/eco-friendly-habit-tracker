-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 06, 2026 at 06:05 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `midproj`
--

-- --------------------------------------------------------

--
-- Table structure for table `habit`
--

CREATE TABLE `habit` (
  `id` int(11) NOT NULL,
  `title` varchar(150) NOT NULL,
  `category` varchar(50) NOT NULL,
  `frequency` varchar(20) DEFAULT NULL,
  `eco_points` int(11) NOT NULL,
  `co2_saved` float DEFAULT NULL,
  `completed` tinyint(1) DEFAULT NULL,
  `streak` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `habit`
--

INSERT INTO `habit` (`id`, `title`, `category`, `frequency`, `eco_points`, `co2_saved`, `completed`, `streak`, `user_id`) VALUES
(1, 'Reusable Water Bottle', 'water', 'Daily', 15, 0.4, 1, 2, 1),
(2, 'Biked / Walked', 'transport', 'Daily', 35, 2.4, 1, 2, 1),
(3, 'Reusable Bag Used', 'waste', 'Daily', 15, 0.3, 1, 2, 1),
(4, 'Power Conserved', 'energy', 'Daily', 20, 1.1, 1, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `username` varchar(80) NOT NULL,
  `password` varchar(120) NOT NULL,
  `points` int(11) DEFAULT NULL,
  `streak` int(11) DEFAULT NULL,
  `co2` float DEFAULT NULL,
  `water` int(11) DEFAULT NULL,
  `waste` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `username`, `password`, `points`, `streak`, `co2`, `water`, `waste`) VALUES
(1, 'kenrut', 'kenrut', 'kenrut123', 110, 1, 5.7, 35, 1.8);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `habit`
--
ALTER TABLE `habit`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `habit`
--
ALTER TABLE `habit`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `habit`
--
ALTER TABLE `habit`
  ADD CONSTRAINT `habit_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
