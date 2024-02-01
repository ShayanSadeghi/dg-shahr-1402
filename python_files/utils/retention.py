import sqlite3
from tqdm import tqdm


# TODO: use a dictionary with 'year-month' as keys to reduce calculations
# TODO: year-month field in final table is defined unique, so we need to check table results before do the calculations,
#       and also we need to be able to update the result for the final month
def retention_calc(db_file):
    con = sqlite3.connect(db_file)

    cur = con.cursor()

    cur.execute(
        """
        select distinct
        STRFTIME('%Y-%m-%d', date(createdAt,'start of month')) as current_month,
        STRFTIME('%Y-%m-%d', date(createdAt,'start of month','+1 month')) as end_of_current_month,
        STRFTIME('%Y-%m-%d', date(createdAt,'start of month','-1 month')) as prev_month
        FROM orders
        ORDER BY current_month
        """
    )

    dts = cur.fetchall()
    for rec in tqdm(dts, "calculate m1-retention rates"):
        # N
        current_month_customers = f""" 
            select count(distinct userId)
            from orders
            where STRFTIME('%Y-%m-%d', date(createdAt, 'start of month')) = ?
        """
        current_month_customers = cur.execute(
            current_month_customers, (rec[0],)
        ).fetchone()[0]

        # S
        prev_month_customers = f""" 
            select count(distinct userId)
            from orders
            where STRFTIME('%Y-%m-%d', date(createdAt, 'start of month')) = ?
        """
        prev_month_customers = cur.execute(prev_month_customers, (rec[2],)).fetchone()[
            0
        ]

        # E
        two_month_customers = f""" 
            select count(distinct userId)
            from orders
            where STRFTIME('%Y-%m-%d', date(createdAt, 'start of month')) >= ? 
                AND STRFTIME('%Y-%m-%d', date(createdAt, 'start of month')) < ?
        """
        two_month_customers = cur.execute(
            two_month_customers, (rec[2], rec[1])
        ).fetchone()[0]

        retention_rate = None
        try:
            # 1- ((E-N)/S)
            retention_rate = 1 - (
                (two_month_customers - current_month_customers) / prev_month_customers
            )
            retention_rate
        except:
            print("no data for previous month")
        yield rec[0], retention_rate

    cur.close()
