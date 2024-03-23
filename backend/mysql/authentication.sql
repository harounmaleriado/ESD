-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Mar 23, 2024 at 06:03 AM
-- Server version: 5.7.39
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `authentication`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `created_at`, `updated_at`) VALUES
(1, 'tshaun', 'abc@xyz.com', 'scrypt:32768:8:1$PuOvlc8lXcwalsOy$5519a960c9537edfad6919485dfb22676774cecd375b2c0b118954a13877eb538b872445ff9912628eae52794b4e40ddaae2ac1ced0e2cfc7cfb7d6ec6468bef', '2024-03-11 05:19:33', '2024-03-11 05:19:33'),
(2, 'admin', 'abcd@xyz.com', 'scrypt:32768:8:1$FMJZLnau6tClbrBi$e028f38428756c72cb021b9a593cfbea10e9e4b40d0f7314472e762a0ce802fb5246911ebd0e012a80988f59cec2aee8ab99346fbf4b4efcd91ebcc063aaa2df', '2024-03-12 07:31:36', '2024-03-12 07:31:36'),
(3, 'admin2', 'abcde@xyz.com', 'scrypt:32768:8:1$P8uptWWlwLn1Zo81$308c801f683868ef33465007458c67c5b79400fe8539d9ea7b9ca454e7b26807b59928a026aed92221387fcf826a880b8b788b3311160de761f7af0bde78ee10', '2024-03-12 08:00:32', '2024-03-12 08:00:32'),
(4, 'admin3', 'abcded@xyz.com', 'scrypt:32768:8:1$3fEhKdyfbKT3wGcL$2d8242b896c7a9eba8f25aeda2dedc6bef3c21c0ca19090d79e64d2f9d5a6faeebc93bdc23332c92e05e73ae730e7ae0ccfc2f38c8b2577ced5e3c1dc086e117', '2024-03-12 09:59:13', '2024-03-12 09:59:13'),
(5, 'orguser', 'fakeman@org.com', 'scrypt:32768:8:1$ieApdIzEbWGcVSDy$167fd5d5ed407e2e40a73282a5fe88aaef2339a9fe3b10e300263aba4dc78e4e32be627b196696ac6890c37a3b4e7035cf20126d7689a1e13281231446ad59db', '2024-03-19 04:31:58', '2024-03-19 04:31:58');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
