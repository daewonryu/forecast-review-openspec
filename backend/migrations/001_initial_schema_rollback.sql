-- Rollback script for migration 001_initial_schema
-- This script removes all tables created in the initial schema

DROP TABLE IF EXISTS insights;
DROP TABLE IF EXISTS simulation_results;
DROP TABLE IF EXISTS drafts;
DROP TABLE IF EXISTS personas;
DROP TABLE IF EXISTS users;
