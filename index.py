from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key
from datetime import datetime

demo_table = resource("dynamodb").Table("practice-dynamo-python")

def insert():
    print(f"demo_insert")
    response = demo_table.put_item(
        Item = {
            "customer_id" : "cus-05", # partition key
            "order_id" : "ord-4", # sort key
            "status" : "pending",
            "created_date" : datetime.now().isoformat()
        }
    )
    print(f"Insert response: {response}")

def select_scan():
    print(f"demo_select_scan")
    filter_expression = Attr("status").eq("pending")

    item_list = []
    dynamo_response = {"LastEvaluatedKey": False}
    while "LastEvaluatedKey" in dynamo_response:
        if dynamo_response["LastEvaluatedKey"]:
            dynamo_response = demo_table.scan(
                FilterExpression = filter_expression,
                ExclusiveStartKey = dynamo_response["LastEvaluatedKey"]
            )
            print(f"response-if {dynamo_response}")
        else:
            dynamo_response = demo_table.scan(
                FilterExpression = filter_expression,
            )
            print(f"response-else: {dynamo_response}")

        for i in dynamo_response["Items"]:
            item_list.append(i)

    print(f"Number of input tasks to process: {len(item_list)}")
    for item in item_list:
        print(f"Item: {item}")

def query_by_partition_key(customer_value):
    print(f"demo_select_query")
    response = {}
    filtering_exp = Key("customer_id").eq(customer_value)
    response = demo_table.query(
        KeyConditionExpression = filtering_exp
    )
    
    # print(f"Query response: {response}")
    # print(f"Query response: {response['Items']}")

    item_list = response["Items"]
    for item in item_list:
        print(f"Item: {item}")

def query_by_partition_key_order(customer_value):
    print(f"\n\t\t\t>>>>>>>>>>>> demo_query_by_partition_key_order <<<<<<<<<<<<<<<")
    response = {}
    filtering_exp = Key("customer_id").eq(customer_value)
    response = demo_table.query(
        KeyConditionExpression = filtering_exp,
        ScanIndexForward = False
    )

    item_list = response["Items"]
    for item in item_list:
        print(f"Item: {item}")

def query_by_index_key(status_value):
    print(f"\n\t\t\t>>>>>>>>>>>> demo_query_by_index_key <<<<<<<<<<<<<<<")

    filtering_exp = Key("status").eq(status_value)
    response = demo_table.query(
        IndexName = "status-index",
        KeyConditionExpression = filtering_exp,
        ScanIndexForward = False
    )

    for item in response["Items"]:
        print(f"Item: {item}")

def query_by_partition_key_and_sort_key(customer_value, order_value):
    print(f"\n\t\t\t>>>>>>>>>>>> demo_query_by_partition_key_and_sort_key <<<<<<<<<<<<<<<")

    response = {}
    filtering_exp = Key("customer_id").eq(customer_value)
    filtering_exp2 = Key("order_id").eq(order_value)
    response = demo_table.query(
        KeyConditionExpression = filtering_exp & filtering_exp2
    )

    for item in response["Items"]:
        print(f"Item: {item}")

def update(customer_value, status_value):
    print(f"\n\t\t\t>>>>>>>>>>>> demo_update <<<<<<<<<<<<<<<")
    response = demo_table.update_item(
        Key = {
            "customer_id": customer_value,
        },
        UpdateExpression = "set status=:r, updated_date=:d",
        ExpressionAttributeValues = {
            ":r": status_value,
            ":d": datetime.now().isoformat()
        },
        ReturnValues = "UPDATED_NEW"
    )

def update_with_expression_name(customer_value, status_value):
    print(f"\n\t\t\t>>>>>>>>>>>> demo_update_with_expression_name <<<<<<<<<<<<<<<")
    response = demo_table.update_item(
        Key = {
            "customer_id": customer_value,
            "order_id": "ord-3"
        },
        UpdateExpression = "set #status=:r, updated_date=:d",
        ExpressionAttributeValues = {
            ":r": status_value,
            ":d": datetime.now().isoformat()
        },
        ExpressionAttributeNames = {
            "#status": "status"
        },
        ReturnValues = "UPDATED_NEW"
    )
    print(f"Response: {response}")

def batch_delete_transaction_records(items_to_delete):
    print(f"Deleting transactions")
    response = {}
    with demo_table.batch_writer() as batch:
        for item in items_to_delete:
            response = batch.delete_item(
                Key = {
                    "customer_id": item["id"], # Change key and value names
                    "order_id": item["order-id"]
                }
            )

items = [{"id": "cus-04", "order-id": "ord-4"}, {"id": "cus-05", "order-id": "ord-4"}]

batch_delete_transaction_records(items)