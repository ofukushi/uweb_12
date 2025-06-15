
# To sync the following tables from Heroku to Render:
#     dividend
#     growth
#     recordhigh
#     value
# You can use pg_dump and psql to export from Heroku and import into Render.
# It:
# Dumps tables from Heroku.
# Drops and imports into:
#     Render database
#     Local database (optional: uncomment if needed)
# Save this as sync_heroku_to_others.sh and run with:
# bash sync_heroku_to_others.sh


#!/bin/bash

# sync_heroku_to_others.sh
# This script syncs tables from a Heroku PostgreSQL database to a Render database (and optionally Local), preserving ID values.

# === Configuration ===
HEROKU_DB_URL="postgres://u4gfsf6lr4e5sj:p37e834285e1c5161de955adf23c5304df5878d00cb78847100ffac916c995840@ceqbglof0h8enj.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d1kmc11fnhb6np"
# RENDER_DB_URL="postgresql://render_postgres_00yz_user:BuMoXameT4MOFv4CA5P2QOfNFvo0pDpF@dpg-d0kg45ogjchc73ad27i0-a/render_postgres_00yz"
External_RENDER_DB_URL=postgresql://render_postgres_00yz_user:BuMoXameT4MOFv4CA5P2QOfNFvo0pDpF@dpg-d0kg45ogjchc73ad27i0-a.singapore-postgres.render.com/render_postgres_00yz
LOCAL_DB_URL=postgresql://postgres_ubuntu:55@localhost:5432/postgres_ubuntu_db

TABLES=(dividend growth recordhigh value)
DUMP_FILE="heroku_dump.sql"

# === Step 1: Dump full table schema and data from Heroku ===
echo "📦 Dumping tables from Heroku (schema + data)..."
pg_dump --clean --if-exists --no-owner --no-privileges \
  "${TABLES[@]/#/--table=}" \
  "$HEROKU_DB_URL" > "$DUMP_FILE"

# === Step 2: Replace in Render ===
echo "🧹 Replacing tables in Render..."
psql "$External_RENDER_DB_URL" < "$DUMP_FILE"

# === Step 3: Ensure ID column is fully populated ===
echo "🔧 Fixing ID columns in Render..."
for table in "${TABLES[@]}"; do
  psql "$External_RENDER_DB_URL" <<EOF
WITH numbered AS (
  SELECT ctid, row_number() OVER () AS new_id FROM $table
)
UPDATE $table
SET id = numbered.new_id
FROM numbered
WHERE $table.ctid = numbered.ctid;
EOF
done

# === Step 4: Reset sequences in Render ===
echo "🔁 Resetting sequences in Render..."
for table in "${TABLES[@]}"; do
  psql "$External_RENDER_DB_URL" <<EOF
SELECT setval(
  pg_get_serial_sequence('$table', 'id'),
  COALESCE((SELECT MAX(id) FROM $table), 1),
  true
);
EOF
done

# === Step 5: Replace Local (optional) ===
Uncomment if needed
echo "🧹 Replacing tables in Local..."
psql "$LOCAL_DB_URL" < "$DUMP_FILE"

echo "🔧 Fixing ID columns in Local..."
for table in "${TABLES[@]}"; do
  psql "$LOCAL_DB_URL" <<EOF
WITH numbered AS (
  SELECT ctid, row_number() OVER () AS new_id FROM $table
)
UPDATE $table
SET id = numbered.new_id
FROM numbered
WHERE $table.ctid = numbered.ctid;
EOF
done

echo "🔁 Resetting sequences in Local..."
for table in "${TABLES[@]}"; do
  psql "$LOCAL_DB_URL" <<EOF
SELECT setval(
  pg_get_serial_sequence('$table', 'id'),
  COALESCE((SELECT MAX(id) FROM $table), 1),
  true
);
EOF
done

echo "✅ Sync from Heroku complete."

# Cleanup
rm -f "$DUMP_FILE"
echo "🗑️ Temporary files cleaned up."