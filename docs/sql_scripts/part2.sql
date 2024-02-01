-------<< PART-2 >>-------
--q1
SELECT AVG(daily_sum) as avg_daily, AVG(
CASE 
	when currency='sek' then ord.sales*0.8
	else ord.sales
END) AS avg_exchanged,
CASE 
	WHEN hld.holyDate IS NULL THEN 'Regular Day'
	ELSE 'Holiday'
END AS day_type
FROM orders ord 
JOIN (
    SELECT 
        date(createdAt) as daily_date,
        SUM(quantity) AS daily_sum
    FROM 
        orders 
    GROUP BY 
        daily_date
) as subq
ON date(ord.createdAt) = subq.daily_date
LEFT JOIN holidays hld 
ON SUBSTR(ord.createdAt,0,11)  = hld.holyDate
GROUP BY day_type

 

--q2
SELECT COUNT(DISTINCT SUBSTR(ord.createdAt,0,11)) as all_days,  COUNT(DISTINCT ord.providerId),COUNT(DISTINCT ord.userid),  
SUM(
CASE 
	when currency='sek' then ord.sales*0.09
	else ord.sales
END)/COUNT(DISTINCT SUBSTR(ord.createdAt,0,11))  as total_sales,
CASE 
	WHEN hld.holyDate IS NULL THEN 'Regular Day'
	ELSE 'Holiday'
END AS day_type
FROM orders ord 
LEFT JOIN holidays hld 
ON SUBSTR(ord.createdAt,0,11)  = hld.holyDate
GROUP BY day_type



