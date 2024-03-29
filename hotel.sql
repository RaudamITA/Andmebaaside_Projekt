SET foreign_key_checks = 0;

DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `hotels`;
DROP TABLE IF EXISTS `rooms`;
DROP table IF EXISTS `hotel_admins`;
DROP TABLE IF EXISTS `hotel_amenities`;
DROP TABLE IF EXISTS `room_amenities`;
DROP TABLE IF EXISTS `hotel_pictures`;
DROP TABLE IF EXISTS `bookings`;

SET foreign_key_checks = 1;

CREATE TABLE IF NOT EXISTS `users` (
	`id` INT(10) AUTO_INCREMENT,
	`username` VARCHAR(50) NOT NULL,
	`hashed_password` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `first_name` VARCHAR(50),
    `last_name` VARCHAR(50),
    `phone` VARCHAR(50),
    `address` VARCHAR(100),
	PRIMARY KEY (`id`),
	UNIQUE (username, email, phone)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `hotels` (
	`id` INT(10) AUTO_INCREMENT,
	`name` VARCHAR(50) NOT NULL,
	`story_count` INT(4) NOT NULL,
	`stars` INT(2) NOT NULL,
	`address` VARCHAR(100) NOT NULL,
    `phone` VARCHAR(50) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `website` VARCHAR(100),
    `description` VARCHAR(1000),
	PRIMARY KEY (`id`),
	UNIQUE (`name`, `address`, `phone`, `email`, `website`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `rooms` (
	`id` INT(10) AUTO_INCREMENT,
    `hotel_id` INT(10) NOT NULL,
	`type` VARCHAR(50) NOT NULL,
	`price` INT(10) NOT NULL,
	`bed_count` INT(2) NOT NULL,
	`ext_bed_count` INT(3) NOT NULL,
    `room_number` INT(10),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `hotel_admins` (
	`id` INT(10) auto_increment,
	`user_id` INT(10) NOT NULL,
	`master_id` INT(10),
	`hotel_id` INT(10) NOT NULL,
	`role` VARCHAR(50) NOT NULL,
	`create_permission` TINYINT(1),
    `read_permission` TINYINT(1),
    `update_permission` TINYINT(1),
    `delete_permission` TINYINT(1),
	PRIMARY	KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `hotel_amenities` (
	`id` INT(15) AUTO_INCREMENT,
	`type` VARCHAR(50) NOT NULL,
	`hotel_id` INT(10),
	`amenity` VARCHAR(100),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `room_amenities` (
	`id` INT(15) AUTO_INCREMENT,
	`room_id` INT(10),
	`amenity` VARCHAR(100),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `hotel_pictures` (
	`id` INT(15) AUTO_INCREMENT,
	`hotel_id` INT(10),
	`url` LONGTEXT,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `bookings` (
    `id` INT(10) AUTO_INCREMENT,
    `user_id` INT(10) NOT NULL,
    `hotel_id` INT(10) NOT NULL,
    `room_id` INT(10) NOT NULL,
    `check_in` VARCHAR(20) NOT NULL,
    `check_out` VARCHAR(20) NOT NULL,
    `adult_count` INT(2) NOT NULL,
    `child_count` INT(2) NOT NULL,
    `total_price` FLOAT(10, 2) NOT NULL,
    `status` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`id`)

) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `log` (
	`id` INT(10) AUTO_INCREMENT,
	`who` VARCHAR(50) NOT NULL,
	`what` VARCHAR(500) NOT NULL,
	`when` VARCHAR(10) NOT NULL,
	`status` VARCHAR(3) NOT NULL,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB;

ALTER TABLE `rooms` ADD FOREIGN KEY (`hotel_id`) REFERENCES `hotels`(`id`);
ALTER TABLE `hotel_admins` ADD FOREIGN KEY (`master_id`) REFERENCES `users`(`id`);
ALTER TABLE `hotel_admins` ADD FOREIGN KEY (`hotel_id`) REFERENCES `hotels`(`id`);
ALTER TABLE `hotel_amenities` ADD FOREIGN KEY (`hotel_id`) REFERENCES `hotels`(`id`);
ALTER TABLE `room_amenities` ADD FOREIGN KEY (`room_id`) REFERENCES `rooms`(`id`);
ALTER TABLE `hotel_pictures` ADD FOREIGN KEY (`hotel_id`) REFERENCES `hotels`(`id`);
ALTER TABLE `bookings` ADD FOREIGN KEY (`user_id`) REFERENCES `users`(`id`);
ALTER TABLE `bookings` ADD FOREIGN KEY (`hotel_id`) REFERENCES `hotels`(`id`);
ALTER TABLE `bookings` ADD FOREIGN KEY (`room_id`) REFERENCES `rooms`(`id`);
