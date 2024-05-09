from google.cloud import bigquery

client = bigquery.Client()

# Perform a query.
QUERY = ('select * from `project1.schema1.table1` LIMIT 100')
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print(row.ROW_ID)
