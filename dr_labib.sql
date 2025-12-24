-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 24, 2025 at 05:34 AM
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
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `status` enum('scheduled','completed','cancelled') DEFAULT 'scheduled',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`id`, `patient_id`, `doctor_id`, `appointment_date`, `appointment_time`, `reason`, `status`, `created_at`) VALUES
(1, 20, 28, '2025-12-25', '10:00:00', 'I think that my issue is that i have pain in my back.', 'scheduled', '2025-12-24 04:27:05'),
(2, 20, 28, '2025-12-25', '10:28:00', 'I am feeling bad.', 'cancelled', '2025-12-24 04:29:02'),
(3, 29, 28, '2025-12-25', '10:30:00', 'I am sick.', 'cancelled', '2025-12-24 04:30:20');

-- --------------------------------------------------------

--
-- Table structure for table `conversations`
--

CREATE TABLE `conversations` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `status` enum('pending','responded','closed') DEFAULT 'pending',
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `is_deleted_by_patient` tinyint(1) DEFAULT 0,
  `is_deleted_by_doctor` tinyint(1) DEFAULT 0,
  `deleted_at_patient` timestamp NULL DEFAULT NULL,
  `deleted_at_doctor` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `conversations`
--

INSERT INTO `conversations` (`id`, `patient_id`, `doctor_id`, `status`, `timestamp`, `updated_at`, `is_deleted_by_patient`, `is_deleted_by_doctor`, `deleted_at_patient`, `deleted_at_doctor`) VALUES
(2, 30, 28, 'pending', '2025-12-19 17:53:47', '2025-12-24 03:13:52', 0, 0, NULL, NULL),
(4, 20, 28, 'responded', '2025-12-24 02:46:46', '2025-12-24 03:14:13', 0, 0, NULL, NULL),
(5, 20, 28, 'responded', '2025-12-24 03:16:29', '2025-12-24 03:17:23', 0, 0, NULL, NULL),
(6, 20, 28, 'pending', '2025-12-24 04:10:39', '2025-12-24 04:11:08', 0, 0, NULL, NULL),
(7, 20, 28, 'pending', '2025-12-24 04:22:04', '2025-12-24 04:22:04', 0, 0, NULL, NULL),
(8, 20, 28, 'pending', '2025-12-24 04:22:26', '2025-12-24 04:22:26', 0, 0, NULL, NULL);

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
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `conversation_id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `sender_role` enum('patient','doctor') NOT NULL,
  `message_type` enum('text','video') DEFAULT 'text',
  `message_text` text DEFAULT NULL,
  `video_path` varchar(255) DEFAULT NULL,
  `translated_text` text DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `is_deleted` tinyint(1) DEFAULT 0,
  `deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`id`, `conversation_id`, `sender_id`, `sender_role`, `message_type`, `message_text`, `video_path`, `translated_text`, `timestamp`, `is_deleted`, `deleted_at`) VALUES
(1, 4, 28, 'doctor', 'text', 'hi, this is a logical error.', NULL, NULL, '2025-12-24 03:14:13', 0, NULL),
(4, 5, 20, 'patient', 'video', NULL, '/static/uploads/signs_videos/patient_20_1766546189.webm', 'I injured my leg and cannot walk properly', '2025-12-24 03:16:29', 0, NULL),
(5, 5, 20, 'patient', 'text', 'HI why you didn\'t respnse?', NULL, NULL, '2025-12-24 03:16:54', 0, NULL),
(6, 5, 28, 'doctor', 'text', 'sorry I was busy.', NULL, NULL, '2025-12-24 03:17:23', 0, NULL),
(7, 6, 20, 'patient', 'video', NULL, '/static/uploads/signs_videos/patient_20_1766549439.webm', 'I have severe headache and fever since yesterday', '2025-12-24 04:10:39', 0, NULL),
(8, 6, 20, 'patient', 'text', 'hey doctor you give me more details of the problem.', NULL, NULL, '2025-12-24 04:11:08', 1, '2025-12-24 04:11:16'),
(9, 7, 20, 'patient', 'video', NULL, '/static/uploads/signs_videos/patient_20_1766550124.webm', 'I injured my leg and cannot walk properly', '2025-12-24 04:22:04', 0, NULL),
(10, 8, 20, 'patient', 'video', NULL, '/static/uploads/signs_videos/patient_20_1766550146.webm', 'I injured my leg and cannot walk properly', '2025-12-24 04:22:26', 0, NULL);

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
(20, 'Umar Kalyal', 'umar4@gmail.com', '0551234521', 'pbkdf2:sha256:1000000$cnT0VT4EpGVATyyg$677a392395f8e29bfe523aff205a51599ef9baa4fc26598eab9f336ccce4f16b', 'patient', '2003-06-24', 'male', '/static/uploads/profile_pics/profile_20_1766549509.jpeg', '2025-12-18 00:50:17'),
(22, 'Dr. Ahmed', 'doctor1@drlabib.com', '+0551234532', '123456', 'doctor', NULL, NULL, NULL, '2025-12-18 01:44:51'),
(23, 'Dr. Ali', 'doctor2@drlabib.com', '+0551234533', '123456', 'doctor', NULL, NULL, NULL, '2025-12-18 01:44:51'),
(24, 'Dr. Awais', 'doctor3@drlabib.com', '+0551234534', '123456', 'doctor', NULL, NULL, NULL, '2025-12-18 01:44:51'),
(25, 'Dr. Ayesha', 'doctor4@drlabib.com', '+0551234535', '123456', 'doctor', NULL, NULL, NULL, '2025-12-18 01:44:51'),
(26, 'Dr. Amber', 'dr5@drlabib.com', '0551234583', 'pbkdf2:sha256:1000000$pLanzlqZNgPgimNR$e9f36e124314d9bab19557f9df26925811d5cfd79e4f4acffa55f21027b0790e', 'patient', NULL, NULL, NULL, '2025-12-18 01:46:56'),
(28, 'Dr. Arooj', 'doctor5@drlabib.com', '0551234591', 'pbkdf2:sha256:1000000$FyNfr4yC9twFqlzi$d0c7f29d45396827d0ed2b11278861866d0d980f2c26324607ace116afa0db89', 'doctor', '1998-01-01', 'female', '/static/uploads/profile_pics/profile_28_1766166943.jpeg', '2025-12-18 01:48:56'),
(29, 'Kalyal', 'umar5@gmail.com', '0551234245', 'pbkdf2:sha256:1000000$rFxksd4d2Evnf3lG$0204cd05d768b6d632f8413e6dd56201ebe9d1a25d9f2fa3c96cc2916d9b504c', 'patient', '2004-01-01', 'male', NULL, '2025-12-18 02:38:28'),
(30, 'Sarah Ba Wazir', 'darkjatt1234@gmail.com', '0551234545', 'pbkdf2:sha256:1000000$opLtnGoOZBZoDs8F$dbe2be35cbf91b271c36636a3a0e51e28962505d61b7f7da131de978f2172ed8', 'patient', NULL, NULL, NULL, '2025-12-19 17:53:05');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_patient` (`patient_id`),
  ADD KEY `idx_doctor` (`doctor_id`),
  ADD KEY `idx_date` (`appointment_date`),
  ADD KEY `idx_status` (`status`);

--
-- Indexes for table `conversations`
--
ALTER TABLE `conversations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_patient` (`patient_id`),
  ADD KEY `idx_doctor` (`doctor_id`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_deleted_patient` (`patient_id`,`is_deleted_by_patient`),
  ADD KEY `idx_deleted_doctor` (`doctor_id`,`is_deleted_by_doctor`);

--
-- Indexes for table `medical_signs`
--
ALTER TABLE `medical_signs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `word_english` (`word_english`),
  ADD KEY `idx_word` (`word_english`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_conversation` (`conversation_id`),
  ADD KEY `idx_sender` (`sender_id`),
  ADD KEY `idx_timestamp` (`timestamp`),
  ADD KEY `idx_deleted` (`conversation_id`,`is_deleted`);

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
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `conversations`
--
ALTER TABLE `conversations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `medical_signs`
--
ALTER TABLE `medical_signs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `conversations`
--
ALTER TABLE `conversations`
  ADD CONSTRAINT `conversations_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `conversations_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
