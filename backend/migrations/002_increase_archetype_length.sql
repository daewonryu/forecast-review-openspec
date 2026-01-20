-- FanEcho MVP Database Schema Migration
-- Migration: 002_increase_archetype_length
-- Created: 2026-01-20
-- Description: Increase archetype column length to accommodate LLM-generated content

ALTER TABLE personas MODIFY COLUMN archetype VARCHAR(100) NOT NULL;
