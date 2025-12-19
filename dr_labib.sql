-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 19, 2025 at 03:14 PM
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
-- Database: `dr_labib`
--

-- --------------------------------------------------------

--
-- Table structure for table `conversations`
--

CREATE TABLE `conversations` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `patient_video_path` varchar(255) DEFAULT NULL,
  `translated_text` text DEFAULT NULL,
  `doctor_response_text` text DEFAULT NULL,
  `sign_video_path` varchar(255) DEFAULT NULL,
  `status` enum('pending','responded','closed') DEFAULT 'pending',
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `patient_response_text` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `conversations`
--

INSERT INTO `conversations` (`id`, `patient_id`, `doctor_id`, `patient_video_path`, `translated_text`, `doctor_response_text`, `sign_video_path`, `status`, `timestamp`, `patient_response_text`) VALUES
(1, 20, 28, '/static/uploads/signs_videos/patient_20_1766025211.webm', 'I injured my leg and cannot walk properly', 'Hey, you need to take some rest.', NULL, 'responded', '2025-12-18 02:33:31', 'ok doctor I\'ll keep it in mind.');

-- --------------------------------------------------------

--
-- Table structure for table `medical_signs`
--

CREATE TABLE `medical_signs` (
  `id` int(11) NOT NULL,
  `word_english` varchar(50) NOT NULL,
  `word_arabic` varchar(50) DEFAULT NULL,
  `video_path` varchar(255) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `medical_signs`
--

INSERT INTO `medical_signs` (`id`, `word_english`, `word_arabic`, `video_path`, `description`) VALUES
(1, 'pain', 'ألم', 'static/signs_videos/pain.mp4', 'General pain sign'),
(2, 'headache', 'صداع', 'static/signs_videos/headache.mp4', 'Sign for headache'),
(3, 'fever', 'حمى', 'static/signs_videos/fever.mp4', 'Sign for fever'),
(4, 'medicine', 'دواء', 'static/signs_videos/medicine.mp4', 'Sign for taking medicine'),
(5, 'doctor', 'طبيب', 'static/signs_videos/doctor.mp4', 'Sign for doctor');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('patient','doctor') NOT NULL,
  `dob` date DEFAULT NULL,
  `gender` enum('male','female','other') DEFAULT NULL,
  `profile_pic` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `full_name`, `email`, `phone`, `password`, `role`, `dob`, `gender`, `profile_pic`, `created_at`) VALUES
(20, 'Umar Kalyal', 'umar4@gmail.com', '0551234521', 'pbkdf2:sha256:1000000$cnT0VT4EpGVATyyg$677a392395f8e29bfe523aff205a51599ef9baa4fc26598eab9f336ccce4f16b', 'patient', '2003-06-24', 'male', NULL, '2025-12-18 00:50:17'),
(22, 'Dr. Ahmed', 'doctor1@drlabib.com', '+0551234532', '123456', 'doctor', NULL, NULL, NULL, '2025-12-18 01:44:51'),
(23, 'Dr. Ali', 'doctor2@drlabib.com', '+0551234533', '123456', 'doctor', NULL, NULL, NULL, '2025-12-18 01:44:51'),
(24, 'Dr. Awais', 'doctor3@drlabib.com', '+0551234534', '123456', 'doctor', NULL, NULL, NULL, '2025-12-18 01:44:51'),
(25, 'Dr. Ayesha', 'doctor4@drlabib.com', '+0551234535', '123456', 'doctor', NULL, NULL, NULL, '2025-12-18 01:44:51'),
(26, 'Dr. Amber', 'dr5@drlabib.com', '0551234583', 'pbkdf2:sha256:1000000$pLanzlqZNgPgimNR$e9f36e124314d9bab19557f9df26925811d5cfd79e4f4acffa55f21027b0790e', 'patient', NULL, NULL, NULL, '2025-12-18 01:46:56'),
(28, 'Dr. Arooj', 'doctor5@drlabib.com', '0551234591', 'pbkdf2:sha256:1000000$FyNfr4yC9twFqlzi$d0c7f29d45396827d0ed2b11278861866d0d980f2c26324607ace116afa0db89', 'doctor', '1998-01-01', 'female', '/static/uploads/profile_pics/profile_28_1766037655.png', '2025-12-18 01:48:56'),
(29, 'Kalyal', 'umar5@gmail.com', '0551234245', 'pbkdf2:sha256:1000000$rFxksd4d2Evnf3lG$0204cd05d768b6d632f8413e6dd56201ebe9d1a25d9f2fa3c96cc2916d9b504c', 'patient', NULL, NULL, NULL, '2025-12-18 02:38:28'),
(30, 'umarhasnat', 'umarhasnat3456@gmail.com', '0551234576', 'pbkdf2:sha256:1000000$ttjuijt43yjQTlZH$6c85660da21c8940ec6d7f471d9a33566429d4adbcb8947de4918ce3aa827936', 'patient', NULL, NULL, NULL, '2025-12-19 14:09:25'),
(31, 'sameer nazakat', 'sameernazakat7@gmail.com', '0551234765', 'pbkdf2:sha256:1000000$5iTw31hsOu4NbVuK$413ed152b83d4ef368db16cf770dd5eddeb62767abbb8063c8a4439c8a86f98a', 'patient', NULL, NULL, NULL, '2025-12-19 14:11:29');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `conversations`
--
ALTER TABLE `conversations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_patient` (`patient_id`),
  ADD KEY `idx_doctor` (`doctor_id`),
  ADD KEY `idx_status` (`status`);

--
-- Indexes for table `medical_signs`
--
ALTER TABLE `medical_signs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `word_english` (`word_english`),
  ADD KEY `idx_word` (`word_english`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone` (`phone`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `conversations`
--
ALTER TABLE `conversations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `medical_signs`
--
ALTER TABLE `medical_signs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `conversations`
--
ALTER TABLE `conversations`
  ADD CONSTRAINT `conversations_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `conversations_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
