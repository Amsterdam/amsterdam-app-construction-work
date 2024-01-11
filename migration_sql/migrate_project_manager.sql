-- Export data from old format construction work database
-- Via e.g. pgadmin4

CREATE TABLE IF NOT EXISTS public.tmp_projectmanager
(
    identifier uuid,
    email character varying,
    projects character varying[]
);

-- Import exported CSV into tmp table

-- Recreate project managers
INSERT INTO construction_work_projectmanager (manager_key, email)
SELECT identifier as manager_key, email FROM tmp_projectmanager;

-- Recreate project_manager-project relationships
-- DEPENDENCY: import projects!
INSERT INTO construction_work_projectmanager_projects (projectmanager_id, project_id)
SELECT a.id AS projectmanager_id, p.id AS project_id FROM (
	SELECT m.id, unnest(t.projects) AS project_id FROM tmp_projectmanager t
	LEFT JOIN construction_work_projectmanager m
	ON t.identifier = m.manager_key
) a
LEFT JOIN construction_work_project p
ON a.project_id = p.foreign_id::varchar
WHERE p.id IS NOT NULL
ORDER BY a.id;
