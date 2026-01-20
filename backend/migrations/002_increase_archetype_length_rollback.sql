-- FanEcho MVP Database Schema Migration Rollback
-- Migration: 002_increase_archetype_length_rollback
-- Created: 2026-01-20
-- Description: Rollback archetype column length to original size

ALTER TABLE personas MODIFY COLUMN archetype VARCHAR(50) NOT NULL;
