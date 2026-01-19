# Database Migration Guide

## Running Migrations

### Apply Migration (MySQL)
```bash
mysql -u root -p fanecho < migrations/001_initial_schema.sql
```

### Rollback Migration
```bash
mysql -u root -p fanecho < migrations/001_initial_schema_rollback.sql
```

## Using SQLAlchemy (Development)

For development, you can use SQLAlchemy to create tables:

```python
from app.db import init_db

# Creates all tables defined in models
init_db()
```

## Migration Checklist

- [x] Users table with email unique constraint
- [x] Personas table with foreign key to users
- [x] Drafts table with foreign key to users
- [x] Simulation_results table with foreign keys to drafts and personas
- [x] Insights table (optional) with unique simulation_id
- [x] All CHECK constraints for score ranges (1-10)
- [x] All indexes for query performance
- [x] Cascade delete rules
- [x] Rollback script tested

## Verification Queries

### Check tables exist
```sql
SHOW TABLES;
```

### Verify foreign keys
```sql
SELECT 
    TABLE_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME
FROM 
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE 
    REFERENCED_TABLE_SCHEMA = 'fanecho'
    AND REFERENCED_TABLE_NAME IS NOT NULL;
```

### Verify indexes
```sql
SHOW INDEX FROM personas;
SHOW INDEX FROM simulation_results;
```

### Test constraints
```sql
-- This should fail (loyalty_level out of range)
INSERT INTO personas (user_id, set_id, name, archetype, loyalty_level, core_values, audience_description)
VALUES (1, 'test', 'Test', 'Test', 11, '[]', 'Test');
```
