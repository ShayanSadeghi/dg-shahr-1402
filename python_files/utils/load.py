import sqlite3


def retention_to_db(db_file, recs=[]):
    """
    @recs is a list of tuples, year-month and retention value to write in @db_file
    """
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    # check if db is not exists, create it
    cur.execute(
        """ 
        CREATE TABLE IF NOT EXISTS dg_kpi (
            year_month TEXT UNIQUE,
            retention_rate REAL
            )
        """
    )

    recs = [f"('{rec[0]}', {rec[1]})" for rec in recs]
    recs = ", ".join(recs)

    insert_sql = "INSERT INTO dg_kpi (year_month, retention_rate) VALUES " + recs
    print(insert_sql)
    cur.execute(insert_sql)
    con.commit()
    cur.close()
