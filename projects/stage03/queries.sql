-- PostgreSQL worked schema/query/transaction answer. Creates isolated answer_lab schema.
BEGIN;
CREATE SCHEMA IF NOT EXISTS answer_lab;
CREATE TABLE IF NOT EXISTS answer_lab.customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS answer_lab.categories (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL);
CREATE TABLE IF NOT EXISTS answer_lab.records (
 id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES answer_lab.customers(id),
 category_id INTEGER NOT NULL REFERENCES answer_lab.categories(id), cents BIGINT NOT NULL CHECK(cents>=0));
INSERT INTO answer_lab.customers VALUES(1,'A'),(2,'B'),(3,'C') ON CONFLICT DO NOTHING;
INSERT INTO answer_lab.categories VALUES(1,'Food'),(2,'Books') ON CONFLICT DO NOTHING;
INSERT INTO answer_lab.records VALUES(1,1,1,100),(2,1,2,200),(3,2,1,50) ON CONFLICT DO NOTHING;
COMMIT;
SELECT c.name,r.cents FROM answer_lab.customers c INNER JOIN answer_lab.records r ON r.customer_id=c.id ORDER BY r.id;
SELECT c.name,COALESCE(SUM(r.cents),0) AS total FROM answer_lab.customers c LEFT JOIN answer_lab.records r ON r.customer_id=c.id GROUP BY c.id,c.name ORDER BY c.id;
SELECT customer_id,SUM(cents) FROM answer_lab.records GROUP BY customer_id HAVING SUM(cents)>100;
WITH totals AS (SELECT customer_id,SUM(cents) AS total FROM answer_lab.records GROUP BY customer_id)
SELECT * FROM totals WHERE total>(SELECT AVG(total) FROM totals);
SELECT c.id FROM answer_lab.customers c WHERE NOT EXISTS(SELECT 1 FROM answer_lab.records r WHERE r.customer_id=c.id);
SELECT customer_id FROM answer_lab.records WHERE cents=100 UNION SELECT customer_id FROM answer_lab.records WHERE cents=200;
SELECT id,SUM(cents) OVER(PARTITION BY customer_id ORDER BY id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) FROM answer_lab.records ORDER BY id;
-- Index experiment uses a temporary table, so no permanent course data is changed.
CREATE TEMP TABLE index_experiment AS SELECT n AS id,n%1000 AS customer_id FROM generate_series(1,100000) n;
ANALYZE index_experiment;
EXPLAIN (ANALYZE,BUFFERS) SELECT * FROM index_experiment WHERE customer_id=12;
CREATE INDEX ON index_experiment(customer_id);
ANALYZE index_experiment;
EXPLAIN (ANALYZE,BUFFERS) SELECT * FROM index_experiment WHERE customer_id=12;
BEGIN;
INSERT INTO answer_lab.records VALUES(999999,3,1,25);
ROLLBACK;
SELECT COUNT(*) AS rolled_back_count FROM answer_lab.records WHERE id=999999; -- 0
