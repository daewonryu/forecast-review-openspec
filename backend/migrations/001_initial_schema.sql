-- FanEcho MVP Database Schema
-- Migration: 001_initial_schema
-- Created: 2026-01-14

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Personas table
CREATE TABLE IF NOT EXISTS personas (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    set_id VARCHAR(36) NOT NULL,
    name VARCHAR(50) NOT NULL,
    archetype VARCHAR(50) NOT NULL,
    loyalty_level INT NOT NULL CHECK (loyalty_level BETWEEN 1 AND 10),
    core_values JSON NOT NULL,
    audience_description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_set (user_id, set_id),
    INDEX idx_set_id (set_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Drafts table
CREATE TABLE IF NOT EXISTS drafts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_created (user_id, created_at),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Simulation results table
CREATE TABLE IF NOT EXISTS simulation_results (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    simulation_id VARCHAR(36) NOT NULL,
    draft_id BIGINT NOT NULL,
    persona_id BIGINT NOT NULL,
    trust_score INT NOT NULL CHECK (trust_score BETWEEN 1 AND 10),
    excitement_score INT NOT NULL CHECK (excitement_score BETWEEN 1 AND 10),
    backlash_risk_score INT NOT NULL CHECK (backlash_risk_score BETWEEN 1 AND 10),
    internal_monologue TEXT NOT NULL,
    public_comment TEXT NOT NULL,
    reasoning TEXT,
    status ENUM('success', 'error') DEFAULT 'success',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (draft_id) REFERENCES drafts(id) ON DELETE CASCADE,
    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    INDEX idx_simulation_id (simulation_id),
    INDEX idx_draft (draft_id),
    INDEX idx_persona (persona_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insights table (optional - can be computed on-demand)
CREATE TABLE IF NOT EXISTS insights (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    simulation_id VARCHAR(36) NOT NULL UNIQUE,
    pain_points JSON NOT NULL,
    improvement_tips JSON NOT NULL,
    overall_sentiment ENUM('positive', 'neutral', 'negative') NOT NULL,
    avg_trust DECIMAL(3,1) NOT NULL,
    avg_excitement DECIMAL(3,1) NOT NULL,
    avg_backlash_risk DECIMAL(3,1) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_simulation_id (simulation_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
