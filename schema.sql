-- =====================================================================
-- LuxeCraft Interior Studio - MySQL Database Export Schema
-- Assessment Plan A - Final Project Database Submission
-- Database Engine: MySQL 8.0+ / MariaDB 10.4+
-- Target Database: luxecraft_db
-- =====================================================================

CREATE DATABASE IF NOT EXISTS `luxecraft_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `luxecraft_db`;

-- ---------------------------------------------------------------------
-- Table 1: Users (Admin & Staff Accounts with Hashed Passwords)
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `role` VARCHAR(20) DEFAULT 'admin',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- Table 2: Categories (Service & Portfolio Classifications)
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL UNIQUE,
    `slug` VARCHAR(100) NOT NULL UNIQUE,
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- Table 3: Services (Interior & Architectural Offerings)
-- Foreign Key: category_id -> categories(id) ON DELETE SET NULL
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS `services`;
CREATE TABLE `services` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `category_id` INT DEFAULT NULL,
    `title` VARCHAR(150) NOT NULL,
    `short_desc` VARCHAR(255) NOT NULL,
    `full_desc` TEXT NOT NULL,
    `price` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `price_unit` VARCHAR(50) DEFAULT 'per project',
    `image_url` VARCHAR(255) DEFAULT '/static/uploads/service_default.jpg',
    `is_featured` TINYINT(1) DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_services_category` FOREIGN KEY (`category_id`) 
        REFERENCES `categories` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- Table 4: Gallery (Portfolio Showcase Items)
-- Foreign Key: category_id -> categories(id) ON DELETE SET NULL
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS `gallery`;
CREATE TABLE `gallery` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `category_id` INT DEFAULT NULL,
    `title` VARCHAR(150) NOT NULL,
    `location` VARCHAR(100) DEFAULT 'Local Studio',
    `image_url` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_gallery_category` FOREIGN KEY (`category_id`) 
        REFERENCES `categories` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- Table 5: Team Members (Studio Staff & Designers)
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS `team_members`;
CREATE TABLE `team_members` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `role` VARCHAR(100) NOT NULL,
    `bio` TEXT,
    `email` VARCHAR(100),
    `phone` VARCHAR(30),
    `image_url` VARCHAR(255) DEFAULT '/static/uploads/team_default.jpg',
    `display_order` INT DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- Table 6: Inquiries (Contact Form Submissions & Service Requests)
-- Foreign Key: service_id -> services(id) ON DELETE SET NULL
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS `inquiries`;
CREATE TABLE `inquiries` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `service_id` INT DEFAULT NULL,
    `client_name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `phone` VARCHAR(30),
    `subject` VARCHAR(150) DEFAULT 'General Inquiry',
    `message` TEXT NOT NULL,
    `status` VARCHAR(20) DEFAULT 'Pending', -- Pending, In Review, Contacted, Closed
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_inquiries_service` FOREIGN KEY (`service_id`) 
        REFERENCES `services` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =====================================================================
-- INITIAL SEED DATA
-- =====================================================================

-- Default Admin User: admin / admin123 (Werkzeug generate_password_hash)
INSERT INTO `users` (`username`, `email`, `password_hash`, `role`) VALUES
('admin', 'admin@luxecraft.com', 'scrypt:32768:8:1$uH34J4y82r73X8QW$a59e99a4c519dbd72f10b7849e75529f798e29be1be3ab7201b1b0b5db1e202525aa1ae4f6b1e54bc2e8d1a10052adbb087612f00ae72aefefbdfa35b1d5c22e', 'admin');

-- Initial Categories
INSERT INTO `categories` (`id`, `name`, `slug`, `description`) VALUES
(1, 'Residential Interior', 'residential-interior', 'Bespoke home, luxury apartment, and villa interior design.'),
(2, 'Commercial Design', 'commercial-design', 'High-end office spaces, retail boutiques, and corporate suites.'),
(3, 'Architectural Planning', 'architectural-planning', 'Structural blueprints, 3D modeling, and renovation execution.'),
(4, 'Custom Furniture', 'custom-furniture', 'Handcrafted bespoke furniture and tailored spatial decor.');

-- Initial Services
INSERT INTO `services` (`id`, `category_id`, `title`, `short_desc`, `full_desc`, `price`, `price_unit`, `image_url`, `is_featured`) VALUES
(1, 1, 'Luxury Villa Redesign', 'Complete interior transformation for high-end villas and luxury penthouses.', 'Our signature luxury villa design package includes 3D spatial mapping, custom material sourcing, lighting design, and end-to-end execution managed by certified architects.', 2500.00, 'per project', '/static/uploads/service1.jpg', 1),
(2, 2, 'Modern Corporate Office Workspace', 'Ergonomic, scalable workplace layouts designed to elevate productivity.', 'We design smart, collaboration-focused corporate environments equipped with acoustic paneling, glass partitions, and executive lounge suites.', 1800.00, 'per floor', '/static/uploads/service2.jpg', 1),
(3, 3, '3D Architectural Rendering & Blueprinting', 'Ultra-realistic 4K walkthroughs and structural schematics.', 'Transform raw concepts into photorealistic 3D virtual walkthroughs before physical construction begins. Includes structural assessment and compliance checks.', 950.00, 'per design concept', '/static/uploads/service3.jpg', 1),
(4, 4, 'Bespoke Custom Furniture Crafting', 'Custom handcrafted timber, marble, and velvet interior decor pieces.', 'Tailor-made furniture designed specifically for your space dimensions. Crafted using sustainable teak wood, brushed brass details, and luxury upholstery.', 1200.00, 'per package', '/static/uploads/service4.jpg', 0);

-- Initial Gallery Items
INSERT INTO `gallery` (`id`, `category_id`, `title`, `location`, `image_url`, `description`) VALUES
(1, 1, 'The Emerald Penthouse Suite', 'Downtown Skyline', '/static/uploads/gallery1.jpg', 'Modern minimalist living room featuring floor-to-ceiling glass windows and custom marble hearth.'),
(2, 2, 'Horizon Tech Innovation Hub', 'Tech City Block', '/static/uploads/gallery2.jpg', 'Open-concept co-working ecosystem featuring bio-centric green walls and custom acoustic pods.'),
(3, 1, 'Nordic Minimalist Villa', 'Suburban Estates', '/static/uploads/gallery3.jpg', 'Warm neutral color palettes, natural oak flooring, and custom ambient cove lighting.'),
(4, 3, 'Skyline Glass Pavilion Architecture', 'Coastal Heights', '/static/uploads/gallery4.jpg', 'Futuristic architectural extension integrating passive solar cooling and smart home automation.');

-- Initial Team Members
INSERT INTO `team_members` (`id`, `name`, `role`, `bio`, `email`, `phone`, `image_url`, `display_order`) VALUES
(1, 'Eleanor Vance', 'Principal Architectural Director', 'Over 12 years of experience leading international luxury interior and spatial planning projects.', 'eleanor@luxecraft.com', '+1 (555) 234-5678', '/static/uploads/team1.jpg', 1),
(2, 'Marcus Thorne', 'Senior Commercial Space Designer', 'Specializes in ergonomic corporate office design, sustainable acoustic materials, and spatial flow.', 'marcus@luxecraft.com', '+1 (555) 345-6789', '/static/uploads/team2.jpg', 2),
(3, 'Sophia Al-Mansoor', '3D Visualizer & Color Theorist', 'Award-winning CG artist delivering photorealistic 3D architectural renders and lighting concepts.', 'sophia@luxecraft.com', '+1 (555) 456-7890', '/static/uploads/team3.jpg', 3);

-- Initial Inquiries
INSERT INTO `inquiries` (`id`, `service_id`, `client_name`, `email`, `phone`, `subject`, `message`, `status`) VALUES
(1, 1, 'David Miller', 'david.m@example.com', '+1 (555) 987-6543', 'Villa Renovation Consultation', 'Hi, I would like to schedule an in-person site audit for a 4500 sq ft residential villa renovation next month.', 'In Review'),
(2, 2, 'Sarah Jenkins', 's.jenkins@innovatetech.io', '+1 (555) 876-5432', 'Office Floor Redesign Quote', 'Looking for an initial quote and 3D concept layout for our new headquarters office floor.', 'Pending');
