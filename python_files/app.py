from utils.retention import retention_calc
from utils.load import retention_to_db

new_recs = []
for rec in retention_calc(db_file="../mock_DG.db"):
    # handle none values
    if rec[1] is not None:
        new_recs.append((rec[0], rec[1]))

print("inserting to db")
retention_to_db("../mock_DG.db", new_recs)
