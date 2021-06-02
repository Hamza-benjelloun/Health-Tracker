-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : jeu. 11 mars 2021 à 21:26
-- Version du serveur :  10.4.14-MariaDB
-- Version de PHP : 7.4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `healthtracker`
--

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add patient', 7, 'add_patient'),
(26, 'Can change patient', 7, 'change_patient'),
(27, 'Can delete patient', 7, 'delete_patient'),
(28, 'Can view patient', 7, 'view_patient'),
(29, 'Can add measures', 8, 'add_measures'),
(30, 'Can change measures', 8, 'change_measures'),
(31, 'Can delete measures', 8, 'delete_measures'),
(32, 'Can view measures', 8, 'view_measures'),
(33, 'Can add state', 9, 'add_state'),
(34, 'Can change state', 9, 'change_state'),
(35, 'Can delete state', 9, 'delete_state'),
(36, 'Can view state', 9, 'view_state');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$216000$G2AW36NWZgck$0XuC9Te25UR1vYQpHFQwrrYjjdudq+yYwKaqjF4bZx4=', '2021-03-11 14:32:22.749499', 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2021-03-10 21:47:54.046991');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2021-03-11 09:31:31.068212', '7', 'Benjelloun', 3, '', 7, 1);

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(8, 'HealthTrackerApp', 'measures'),
(7, 'HealthTrackerApp', 'patient'),
(9, 'HealthTrackerApp', 'state'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'HealthTrackerApp', '0001_initial', '2021-03-10 21:45:48.013470'),
(2, 'HealthTrackerApp', '0002_auto_20210308_1131', '2021-03-10 21:45:49.623526'),
(3, 'HealthTrackerApp', '0003_patient_rfid', '2021-03-10 21:45:49.789906'),
(4, 'HealthTrackerApp', '0004_auto_20210309_1705', '2021-03-10 21:45:49.819992'),
(5, 'HealthTrackerApp', '0005_auto_20210309_1741', '2021-03-10 21:45:50.209059'),
(6, 'HealthTrackerApp', '0006_auto_20210309_1742', '2021-03-10 21:45:50.267931'),
(7, 'HealthTrackerApp', '0007_auto_20210309_1744', '2021-03-10 21:45:50.382611'),
(8, 'contenttypes', '0001_initial', '2021-03-10 21:45:51.198786'),
(9, 'auth', '0001_initial', '2021-03-10 21:45:52.820988'),
(10, 'admin', '0001_initial', '2021-03-10 21:46:02.591840'),
(11, 'admin', '0002_logentry_remove_auto_add', '2021-03-10 21:46:04.771504'),
(12, 'admin', '0003_logentry_add_action_flag_choices', '2021-03-10 21:46:04.897726'),
(13, 'contenttypes', '0002_remove_content_type_name', '2021-03-10 21:46:05.702635'),
(14, 'auth', '0002_alter_permission_name_max_length', '2021-03-10 21:46:06.881949'),
(15, 'auth', '0003_alter_user_email_max_length', '2021-03-10 21:46:07.086862'),
(16, 'auth', '0004_alter_user_username_opts', '2021-03-10 21:46:07.126265'),
(17, 'auth', '0005_alter_user_last_login_null', '2021-03-10 21:46:07.977508'),
(18, 'auth', '0006_require_contenttypes_0002', '2021-03-10 21:46:08.037860'),
(19, 'auth', '0007_alter_validators_add_error_messages', '2021-03-10 21:46:08.084830'),
(20, 'auth', '0008_alter_user_username_max_length', '2021-03-10 21:46:08.185338'),
(21, 'auth', '0009_alter_user_last_name_max_length', '2021-03-10 21:46:08.393268'),
(22, 'auth', '0010_alter_group_name_max_length', '2021-03-10 21:46:08.662519'),
(23, 'auth', '0011_update_proxy_permissions', '2021-03-10 21:46:08.715298'),
(24, 'auth', '0012_alter_user_first_name_max_length', '2021-03-10 21:46:08.842993'),
(25, 'sessions', '0001_initial', '2021-03-10 21:46:09.265364'),
(26, 'HealthTrackerApp', '0008_auto_20210310_2311', '2021-03-10 22:11:40.307784'),
(27, 'HealthTrackerApp', '0009_auto_20210310_2321', '2021-03-10 22:22:00.212090'),
(28, 'HealthTrackerApp', '0010_auto_20210310_2322', '2021-03-10 22:22:51.578477'),
(29, 'HealthTrackerApp', '0011_auto_20210310_2329', '2021-03-10 22:29:36.270071'),
(30, 'HealthTrackerApp', '0012_auto_20210311_0254', '2021-03-11 01:54:53.326266'),
(31, 'HealthTrackerApp', '0013_auto_20210311_0258', '2021-03-11 01:59:07.599494'),
(32, 'HealthTrackerApp', '0014_state', '2021-03-11 08:27:18.035339');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('yl1eszig4wwdiuzwsxjjztnepwpngpl8', '.eJxVjMsOwiAQRf-FtSHDI0BduvcbyAwDUjWQlHZl_Hdt0oVu7znnvkTEba1xG3mJM4uzUOL0uxGmR2474Du2W5ept3WZSe6KPOiQ1875eTncv4OKo37rCQAocTFTUUSFPHltwRhHxTCEBCl7AAxOKwvFsnMEnjV6tqEEzuL9AetaOB0:1lKMMQ:nbEUKPdJInesKhm0QKyCz6-ZVL0kCaXaxmILnMV6KiU', '2021-03-25 14:32:22.833575');

-- --------------------------------------------------------

--
-- Structure de la table `healthtrackerapp_measures`
--

CREATE TABLE `healthtrackerapp_measures` (
  `id` int(11) NOT NULL,
  `tension_state` varchar(200) DEFAULT NULL,
  `tension` varchar(200) DEFAULT NULL,
  `temp_state` varchar(200) DEFAULT NULL,
  `temperature` varchar(200) DEFAULT NULL,
  `id_patient` varchar(200) DEFAULT NULL,
  `date_time` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `healthtrackerapp_measures`
--

INSERT INTO `healthtrackerapp_measures` (`id`, `tension_state`, `tension`, `temp_state`, `temperature`, `id_patient`, `date_time`) VALUES
(1, NULL, NULL, NULL, NULL, 'CC 1E 0C 30', '0000-00-00 00:00:00'),
(2, 'HYPERTENSION!', '151/93', 'URGENT!', '17.15', 'D7 68 20 62', '2021-03-11 03:47:26'),
(3, 'Normal', '116/78', 'URGENT!', '1037.55', 'D7 68 20 62', '2021-03-11 03:47:46'),
(4, 'LOW!', '99/94', 'Normal', '32.91', 'D7 68 20 62', '2021-03-11 03:47:52'),
(28, NULL, NULL, NULL, NULL, 'D7 68 20 62', '2021-03-11 08:54:08'),
(29, NULL, NULL, NULL, NULL, 'D7 68 20 62', '2021-03-11 08:54:08'),
(30, NULL, NULL, NULL, NULL, 'D7 68 20 62', '2021-03-11 08:54:10'),
(31, NULL, NULL, NULL, NULL, 'D7 68 20 62', '2021-03-11 08:54:10'),
(32, NULL, NULL, NULL, NULL, 'D7 68 20 62', '2021-03-11 08:54:44'),
(33, NULL, NULL, NULL, NULL, 'D7 68 20 62', '2021-03-11 08:54:44'),
(34, NULL, NULL, NULL, NULL, 'D7 68 20 62', '2021-03-11 08:55:04'),
(35, 'HYPERTENSION!', '140/88', 'URGENT!', '17.51', 'D7 68 20 62', '2021-03-11 10:01:48'),
(36, 'LOW!', '114/50', 'URGENT!', '1037.55', 'D7 68 20 62', '2021-03-11 11:24:44'),
(37, 'Normal', '108/88', 'URGENT!', '18.71', 'D7 68 20 62', '2021-03-11 11:25:08'),
(38, 'HYPERTENSION!', '165/105', 'Normal', '34.39', 'D7 68 20 62', '2021-03-11 11:26:18'),
(39, 'Normal', '134/89', 'Normal', '34.25', 'D7 68 20 62', '2021-03-11 16:06:01'),
(40, 'HYPERTENSION!', '176/85', 'URGENT!', '23.33', 'D7 68 20 62', '2021-03-11 16:07:35'),
(41, 'HYPERTENSION!', '160/69', 'URGENT!', '1037.55', 'D7 68 20 62', '2021-03-11 16:08:26');

-- --------------------------------------------------------

--
-- Structure de la table `healthtrackerapp_patient`
--

CREATE TABLE `healthtrackerapp_patient` (
  `id` int(11) NOT NULL,
  `Firstname` varchar(200) DEFAULT NULL,
  `Lastname` varchar(200) DEFAULT NULL,
  `Cin` varchar(200) DEFAULT NULL,
  `State` varchar(200) NOT NULL,
  `Temperature` varchar(200) DEFAULT NULL,
  `Tension` varchar(200) DEFAULT NULL,
  `date_created` datetime NOT NULL DEFAULT current_timestamp(),
  `RFID` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `healthtrackerapp_patient`
--

INSERT INTO `healthtrackerapp_patient` (`id`, `Firstname`, `Lastname`, `Cin`, `State`, `Temperature`, `Tension`, `date_created`, `RFID`) VALUES
(1, 'asma', 'ben', 'AE34566', 'Sleeping', '34.39', '165/105', '2021-03-10 23:29:51', 'D7 68 20 62');

-- --------------------------------------------------------

--
-- Structure de la table `healthtrackerapp_state`
--

CREATE TABLE `healthtrackerapp_state` (
  `id` int(11) NOT NULL,
  `id_patient` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `healthtrackerapp_state`
--

INSERT INTO `healthtrackerapp_state` (`id`, `id_patient`, `status`) VALUES
(7, 'D7 68 20 62', 'Sleeping'),
(8, 'CC 1E 0C 30', 'Sleeping');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Index pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Index pour la table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Index pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Index pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Index pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Index pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Index pour la table `healthtrackerapp_measures`
--
ALTER TABLE `healthtrackerapp_measures`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_patient` (`id_patient`),
  ADD KEY `id_patient_2` (`id_patient`);

--
-- Index pour la table `healthtrackerapp_patient`
--
ALTER TABLE `healthtrackerapp_patient`
  ADD PRIMARY KEY (`RFID`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Index pour la table `healthtrackerapp_state`
--
ALTER TABLE `healthtrackerapp_state`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT pour la table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT pour la table `healthtrackerapp_measures`
--
ALTER TABLE `healthtrackerapp_measures`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT pour la table `healthtrackerapp_patient`
--
ALTER TABLE `healthtrackerapp_patient`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `healthtrackerapp_state`
--
ALTER TABLE `healthtrackerapp_state`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Contraintes pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Contraintes pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
