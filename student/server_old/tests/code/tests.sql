

SELECT DATE_TRUNC('year', CURRENT_DATE - (n || ' years')::INTERVAL) AS year_start
FROM generate_series(0, 2) AS n
ORDER BY year_start DESC;



SELECT 
    date_trunc('year', last_time) AS year,
    COUNT(*) AS count,
    SUM(mark) AS mark,
    SUM(times) AS times 
FROM polyglots_users.user_content
WHERE last_time > '2000-01-01' 
AND lang = 'el'
AND user_id = 'test_user'
GROUP BY year
ORDER BY year ASC;


-- 5 years of data
select f.year_start, s.year, s.cnt, s.times, s.mark FROM (
	SELECT DATE_TRUNC('year', CURRENT_DATE - (n || ' years')::INTERVAL) AS year_start
	FROM generate_series(0, 5) AS n) as f
left join (
	SELECT 
    date_trunc('year', last_time) AS year,
    COUNT(*) AS cnt,
    SUM(mark) AS mark,
    SUM(times) AS times 
	FROM polyglots_users.user_content
	WHERE last_time > '2000-01-01' 
	AND lang = 'el'
	AND user_id = 'test_user'
	GROUP BY year) as s
on f.year_start = s.year



-- from beginning of the year
select f.month, s.month, s.cnt, s.times, s.mark FROM (
	SELECT DATE_TRUNC('month', CURRENT_DATE - (n || ' months')::INTERVAL) AS month
	FROM generate_series(0, 3) AS n) as f
left join (
	SELECT 
    date_trunc('month', last_time) AS month,
    COUNT(*) AS cnt,
    SUM(mark) AS mark,
    SUM(times) AS times 
	FROM polyglots_users.user_content
	WHERE last_time > '2000-01-01' 
	AND lang = 'el'
	AND user_id = 'test_user'
	GROUP BY month) as s
on f.month = s.month

-- pluggable 

select f.date_interval, s.date_interval, s.cnt, s.times, s.mark FROM (
	SELECT DATE_TRUNC('month', '2025-01-01'::TIMESTAMP + (n || ' months')::INTERVAL) AS date_interval
	FROM generate_series(0, 11) AS n) as f
left join (
	SELECT 
    date_trunc('month', last_time) AS date_interval,
    COUNT(*) AS cnt,
    SUM(mark) AS mark,
    SUM(times) AS times 
	FROM polyglots_users.user_content
	WHERE last_time > '2025-01-01'::TIMESTAMP 
	AND lang = 'el'
	AND user_id = 'test_user'
	GROUP BY date_interval) as s
on f.date_interval = s.date_interval
ORDER BY f.date_interval



LEFT JOIN (
            SELECT 
                date_trunc('{date_unit}s', last_time) AS date_interval,
                COUNT(*) AS cnt1,
                SUM(mark) AS mark1,
                SUM(times) AS times1 
            FROM {req.customer_id}_users.journal
            WHERE last_time > '{start_date}'::TIMESTAMP 
            AND lang = %s
            AND user_id = %s
            GROUP BY date_interval) as s
        ) as journal
        ON f.date_interval = journal.date_interval