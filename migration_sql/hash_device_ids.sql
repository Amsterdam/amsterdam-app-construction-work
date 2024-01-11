-- Extention required for performing "digest('foobar', 'sha256')"

CREATE EXTENSION pgcrypto;

-- Test hashing device_id with SELECT

SELECT encode(digest(device_id, 'sha256'), 'hex')
FROM construction_work_device
WHERE id = 1030;

-- Perform update query on single row
-- Remove WHERE to perform update on all rows
-- Backup 'construction_work_device' table before update!

UPDATE construction_work_device
SET device_id = encode(digest(device_id, 'sha256'), 'hex')
WHERE id = 1030;
