SELECT JSON """{
  "customer_id": "20",
  "first_name": "Anna",
  "last_name": "A.",
  "first_order_date": "2018-01-23",
  "most_recent_order_date": "2018-01-23",
  "number_of_orders": "1"
}"""
;

--Create a Table with JSON as datatype
CREATE TABLE `test.json_table` (customer_info JSON);

-- Insert 2 records
INSERT INTO test.json_table(customer_info) SELECT JSON_ARRAY("""{"customer_id": "20","first_name": "Anna","last_name": "A.","first_order_date": "2018-01-23","most_recent_order_date": "2018-01-23","number_of_orders": "1"}, {"customer_id": "23","first_name": "Mildred""last_name": "A.","first_order_date": null,"most_recent_order_date": null,"number_of_orders": "0"}""");

