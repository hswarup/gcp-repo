—-create a dataset(schema)
bq mk babynames

-—list datasets
bq ls

-—load a file with 3 columns into a BigQuery Table
bq load babynames.names2010 \
    yob2010.txt \
name:string,assigned_sex_at_birth:string,count:integer

-—See the schema and other details
bq show babynames.names2010

--Quey the data
bq query --use_legacy_sql=false \
    'SELECT
      name,
      count
    FROM
      `aqueous-scout-242713.babynames.names2010`
    WHERE
      assigned_sex_at_birth = "M"
    ORDER BY
      count ASC
    LIMIT 5;'
    
--Remove all tables in a dataset
bq rm --recursive=true babynames
