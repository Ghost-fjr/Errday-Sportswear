# Migration Notes - Errday Sportwear

## Migration Status: ⚠️ DEFERRED

### Issue Encountered
During the refactoring process, multiple model fields were enhanced with:
- Database indexes
- Timestamp fields (`created_at`, `updated_at`)
- Field validation improvements
- Model renames (`loginview` → `UserProfile`)

When attempting to create migrations, Django prompted for default values for new fields on existing database records.

### Why Migrations Were Deferred
The existing `db.sqlite3` database contains production/development data. To avoid data loss or complications:
1. Model changes require defaults for existing rows
2. The `UserProfile` model rename is a breaking change
3. Multiple timestamp fields need population

### Recommended Migration Strategy

#### Option 1: Fresh Start (Easiest - Recommended for Development)
```bash
# Backup existing database
copy db.sqlite3 db.sqlite3.backup

# Delete database
Remove-Item db.sqlite3

# Create fresh migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Repopulate data as needed
```

#### Option 2: Preserve Existing Data (Production/Important Data)
```bash
# 1. Backup database
copy db.sqlite3 db.sqlite3.backup

# 2. Create custom migration with data preservation
python manage.py makemigrations --empty store

# 3. Edit the migration file to:
#    - Add new fields as nullable first
#    - Populate existing records with appropriate defaults
#    - Make fields non-nullable after population

# 4. Apply migrations
python manage.py migrate  
```

#### Option 3: Manual SQL Migration
```sql
-- For each new timestamp field:
ALTER TABLE store_size ADD COLUMN created_at DATETIME NULL;
UPDATE store_size SET created_at = datetime('now') WHERE created_at IS NULL;

-- Repeat for other models...
```

### Model Changes Requiring Migration

1. **Size Model**
   - Added: `created_at`
   - Added: database index on `name`

2. **UserProfile Model** (renamed from `loginview`)
   - **BREAKING**: Model renamed
   - Added: phone validator
   - Added: `created_at`, `updated_at`
   - Changed: `type` → `user_type`
   - Changed: ForeignKey → OneToOneField

3. **Customer Model**
   - Added: `created_at`, `updated_at`
   - Changed: `email` from CharField to EmailField
   - Added: composite index on `email` and `name`

4. **Product Model**
   - Added: `description`, `stock`, `is_active`
   - Added: `created_at`, `updated_at`
   - Added: multiple database indexes
   - Changed: size choices (Added XS)

5. **Order Model**
   - Added: `created_at`, `updated_at`
   - Added: database indexes
   - Added: index on `transaction_id`

6. **OrderItem Model**
   - Changed: `order` ForeignKey to CASCADE
   - Added: database indexes

7. **ShippingAddress Model**
   - Added: `country` field (default='USA')
   - Changed: `order` relationship to CASCADE

### Current Database State
The codebase has been refactored with improved models, but migrations have NOT been applied.

**This means:**
- ✅ Code is clean and follows best practices
- ✅ New code uses improved models
- ⚠️ Database schema doesn't match model definitions
- ⚠️ New fields (timestamps, indexes) don't exist in DB
- ⚠️ UserProfile model still named `loginview` in database

### Next Steps

**For Development/Testing:**
1. Delete `db.sqlite3`
2. Run `python manage.py makemigrations`
3.Run `python manage.py migrate`
4. Create test data

**For Production:**
1. Export important data
2. Create custom migration with data preservation
3. Test migration on copy of production database
4. Apply to production with backup

### Files Cleaned Up ✅
The following unnecessary directories were successfully removed:
- `djandoenv/` (6,224 files)
- `djangoenv/` (3 files)
- `envs/` (1,010 files)
- `store/FloderPath/` (1,380 files - numpy installation)

Total space reclaimed: ~8,600+ files

### Working Without Migrations (Temporary)
Until migrations are applied:
- Application will run but may have issues with new features
- Timestamp fields won't be populated
- Indexes won't improve performance
- `UserProfile` references need to use `loginview`

**Bottom Line**: Migrations should be run before production deployment.
