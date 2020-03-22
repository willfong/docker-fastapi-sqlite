import os
import boto3
from botocore.exceptions import ClientError
from ..services import util, statsd


dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION_NAME'), endpoint_url=os.environ.get('DDB_ENDPOINT_URL'))

USERS = dynamodb.Table('Users')
MESSAGES = dynamodb.Table('Messages')

@statsd.statsd_root_stats
def upsert(table, key, expression, names, values, condition=None):
    args = {
        "Key": key, 
        "UpdateExpression": expression,
        "ExpressionAttributeNames": names,
        "ExpressionAttributeValues": values
    }
    if condition:
        args['ConditionExpression'] = condition
    
    try:
        table.update_item(**args)
    except ClientError as e:
        util.logger.error(f"[UPSERT|{table}|{key}] {e}")
        util.logger.error(args)
        return False
    return True

@statsd.statsd_root_stats
def put(table, item):
    try:
        table.put_item(Item=item)
    except ClientError as e:
        util.logger.error(f"[PUT|{table}|{item}] {e}")
        return False
    return True

@statsd.statsd_root_stats
def scan(table, sort=None):
    try:
        response = table.scan()
        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
    except ClientError as e:
        util.logger.error(f"[SCAN|{table}] {e}")
        return False
    if sort:
        data.sort(key=lambda x: x[sort], reverse=True)
    return data

@statsd.statsd_root_stats
def get(table, key):
    try: 
        response = table.get_item(Key=key)
    except ClientError as e:
        util.logger.error(f"[GET|{table}|{key}] {e}")
        return False
    return response.get('Item')

@statsd.statsd_root_stats
def query(table, expression, values):
    try:
        response = table.query(
            KeyConditionExpression=expression,
            ExpressionAttributeValues=values
        )
    except ClientError as e:
        util.logger.error(f"[QUERY|{table}|{expression}] {e}")
        return False
    return response.get('Items')  


'''
DDB Notes:

## Append or Create to list

    key = {'id': users_id}
    expression = "SET #foodies = list_append(if_not_exists(#foodies, :empty_list), :foodie)"
    names = {"#foodies": 'foodies'}
    values = {":empty_list": [], ":foodie": [foodie_id]}

'''