# Quick Migration Commands

## 1. Backup Current SQLite Data
```bash
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > data_backup.json
```

## 2. Set PostgreSQL Connection (Windows PowerShell)
```powershell
# Replace with your actual credentials
$env:DATABASE_URL="postgresql://username:password@host:port/database_name"

# Example for local PostgreSQL:
$env:DATABASE_URL="postgresql://room_booking_user:mypassword@localhost:5432/room_booking_app"
```

## 3. Verify Connection
```bash
# Check which database Django is using
python migrate_helper.py
# Then choose option 1 to show database info
```

## 4. Run Migrations on PostgreSQL
```bash
python manage.py migrate
```

## 5. Load Data into PostgreSQL
```bash
python manage.py loaddata data_backup.json
```

## 6. Verify Migration Success
```bash
python migrate_helper.py
# Then choose option 3 to verify data
```

## 7. Create Superuser (if needed)
```bash
python manage.py createsuperuser
```

## 8. Test the Application
```bash
python manage.py runserver
```

---

## Environment Variable Format

**DATABASE_URL Format:**
```
postgresql://[username]:[password]@[host]:[port]/[database_name]
```

**Examples:**

Local PostgreSQL:
```
postgresql://myuser:mypassword@localhost:5432/room_booking_app
```

Railway (example):
```
postgresql://postgres:password123@containers-us-west-1.railway.app:5432/railway
```

---

## Troubleshooting

**Check current database:**
```bash
python manage.py dbshell
```
- If you see `sqlite>` prompt → Using SQLite
- If you see `postgres=#` or `database=#` prompt → Using PostgreSQL

**Reset migrations (if needed):**
```bash
python manage.py migrate --fake-initial
```

**Check migration status:**
```bash
python manage.py showmigrations
```
