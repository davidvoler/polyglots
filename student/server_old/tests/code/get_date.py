
sql = f"""
select f.date_interval, s.date_interval, s.cnt, s.times, s.mark FROM (
	SELECT DATE_TRUNC('month', '{start_date}' + (n || ' months')::INTERVAL) AS date_interval
	FROM generate_series(0, {steps}) AS n) as f
left join (
	SELECT 
    date_trunc('month', last_time) AS date_interval,
    COUNT(*) AS cnt,
    SUM(mark) AS mark,
    SUM(times) AS times 
	FROM polyglots_users.user_content
	WHERE last_time > '2025-01-01' 
	AND lang = 'el'
	AND user_id = 'test_user'
	GROUP BY date_interval) as s
on f.date_interval = s.date_interval
ORDER BY f.date_interval
"""