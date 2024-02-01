-------<< PART-1 >>-------
-- q1
SELECT usr.id, usr.registeredDate, usr.country, SUM(ord.sales) as total_sales_no_exchange, SUM(
CASE 
	when currency='sek' then ord.sales*0.09	
	else ord.sales
END) as total_sales
from users usr 
JOIN orders ord 
ON usr.id = ord.userId
WHERE STRFTIME('%Y',usr.registeredDate)="2023"
GROUP BY  usr.id, usr.registeredDate, usr.country 
ORDER BY total_sales DESC 
LIMIT 10;

-- q2
SELECT SUM(quantity) as total_quantity, defaultOfferType 
FROM providers 
JOIN orders
ON providers.id = orders.providerId
GROUP BY defaultOfferType
ORDER BY total_quantity DESC 
LIMIT 1;
