
-- reusable SQL function
CREATE OR REPLACE FUNCTION reset_sequential_ids(tablename TEXT) RETURNS void AS $$
DECLARE
    sql TEXT;
BEGIN
    -- Step 1: update IDs using ctid + row_number
    EXECUTE format($f$
        WITH numbered AS (
            SELECT ctid, row_number() OVER () AS new_id FROM %I
        )
        UPDATE %I
        SET id = numbered.new_id
        FROM numbered
        WHERE %I.ctid = numbered.ctid;
    $f$, tablename, tablename, tablename);

    -- Step 2: reset sequence for serial ID
    EXECUTE format($f$
        SELECT setval(
            pg_get_serial_sequence('%I', 'id'),
            COALESCE((SELECT MAX(id) FROM %I), 1),
            true
        );
    $f$, tablename, tablename);
END;
$$ LANGUAGE plpgsql;
