-- Active: 1781681076017@@127.0.0.1@3306@mphasis_db

-- 1. Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS mphasis_db;

-- 2. Switch to the newly created database
USE mphasis_db;

-- 3. Create the tickets table
-- This structure mirrors the SQLAlchemy TicketDB model in crud_app/models/tickets.py
CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(1000),
    priority VARCHAR(50),
    status VARCHAR(50),
    INDEX idx_ticket_id (ticket_id)
);

-- 4. Example: SQL query to save (insert) a new ticket's info
INSERT INTO tickets (ticket_id, title, description, priority, status)
VALUES 
('INC-1', 'Server Outage', 'Main server is down in US-East', 'High', 'open'),
('INC-2', 'Login Issue', 'Users cannot log into the dashboard', 'Medium', 'open');

-- 5. Example: Retrieve all tickets to verify creation
SELECT * FROM tickets;
