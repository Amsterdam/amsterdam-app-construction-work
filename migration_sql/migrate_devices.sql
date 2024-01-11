-- Export data from old format construction work database
-- Via e.g. pgadmin4

CREATE TABLE IF NOT EXISTS public.tmp_firebasetoken
(
    deviceid character varying(200),
    firebasetoken character varying(1000),
    os character varying(7)
);

CREATE TABLE IF NOT EXISTS public.tmp_mobilephoneaccesslog
(
    deviceid character varying(200),
    last_access timestamp with time zone
);

CREATE TABLE IF NOT EXISTS public.tmp_followedproject
(
    id bigint,
    deviceid character varying(200),
    projectid character varying(200)
);

-- Import exported CSV into tmp tables

-- Recreate devices
INSERT INTO construction_work_device (device_id, firebase_token, last_access, os)
SELECT d.deviceid AS device_id, d.firebasetoken AS firebase_token, m.last_access, d.os
FROM tmp_firebasetoken d
LEFT JOIN tmp_mobilephoneaccesslog m
ON d.deviceid = m.deviceid;

-- Recreate device-project relationships
-- DEPENDENCY: import projects!
INSERT INTO construction_work_device_followed_projects (device_id, project_id)
SELECT device_id, project_id FROM (
	SELECT d.id AS device_id, p.id as project_id FROM tmp_followedproject o

	LEFT JOIN construction_work_project p
	ON o.projectid = p.foreign_id::varchar

	LEFT JOIN construction_work_device d
	ON o.deviceid = d.device_id
) x
WHERE device_id IS NOT NULL
AND project_id IS NOT NULL;

-- Find device ids in old followedproject table not found in old firebasetoken table
SELECT d.device_id AS new_device_id, o.deviceid AS old_device_id, p.id as new_project_id FROM tmp_followedproject o

LEFT JOIN construction_work_project p
ON o.projectid = p.foreign_id::varchar

LEFT JOIN construction_work_device d
ON o.deviceid = d.device_id

WHERE d.device_id IS NULL
ORDER BY d.id;
