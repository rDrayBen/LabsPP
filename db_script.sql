CREATE SCHEMA IF NOT EXISTS `online_store` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `online_store` ;

CREATE TABLE IF NOT EXISTS `online_store`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `login` VARCHAR(45) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `phone` VARCHAR(25) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  `is_admin` bool NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `login` (`login` ASC) VISIBLE,
  UNIQUE INDEX `phone` (`phone` ASC) VISIBLE,
  UNIQUE INDEX `email` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `online_store`.`vendor` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `company_name` VARCHAR(45) NOT NULL,
  `location` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `company_name` (`company_name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `online_store`.`good_category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `category_name` (`category_name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `online_store`.`good` (
  `id` INT NOT NULL AUTO_INCREMENT, 
  `vendor_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `cost` INT NOT NULL,
  `num_in_stock` INT NOT NULL,
  `creation_date` DATETIME NOT NULL,
  `is_reserved` bool NOT NULL,
  PRIMARY KEY (`id`, `vendor_id`),
  INDEX `vendor_id` (`vendor_id` ASC) VISIBLE,
  INDEX `category_id` (`category_id` ASC) VISIBLE,
  CONSTRAINT `good_ibfk_1`
    FOREIGN KEY (`vendor_id`)
    REFERENCES `online_store`.`vendor` (`id`)
    ON DELETE cascade
    ON UPDATE cascade,
  CONSTRAINT `good_ibfk_2`
    FOREIGN KEY (`category_id`)
    REFERENCES `online_store`.`good_category` (`id`)
    ON DELETE cascade
    ON UPDATE cascade)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `online_store`.`order` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `good_id` INT NOT NULL,
  `buy_date` DATETIME NOT NULL,
  PRIMARY KEY (`id`, `user_id`, `good_id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  INDEX `fk_order_good1_idx` (`good_id` ASC) VISIBLE,
  CONSTRAINT `order_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `online_store`.`user` (`id`)
    ON DELETE cascade
    ON UPDATE cascade,
  CONSTRAINT `fk_order_good1`
    FOREIGN KEY (`good_id`)
    REFERENCES `online_store`.`good` (`id`)
    ON DELETE cascade
    ON UPDATE cascade)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `online_store`.`delivery` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `type` ENUM('self pickup', 'courier') NOT NULL,
  `from_` VARCHAR(45) NOT NULL,
  `to` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`, `order_id`),
  INDEX `fk_delivery_order1_idx` (`order_id` ASC) VISIBLE,
  CONSTRAINT `fk_delivery_order1`
    FOREIGN KEY (`order_id`)
    REFERENCES `online_store`.`order` (`id`)
    ON DELETE cascade
    ON UPDATE cascade)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;