import json
import boto3
from datetime import datetime
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FeedbackTable')  # 确保表名正确

def lambda_handler(event, context):
    try:
        # 调试：打印原始事件和请求头
        print("Raw event:", json.dumps(event, indent=2))
        
        # 1. 检查请求头 Content-Type 是否为 application/json
        headers = event.get('headers', {})
        # content_type = headers.get('Content-Type', '').lower()
        
        # if 'application/json' not in content_type:
        #     return {
        #         'statusCode': 400,
        #         'body': json.dumps({'error': 'Content-Type must be application/json'})
        #     }
        
        # 2. 解析请求体（兼容代理和非代理模式）
        request_body = event.get('body', {})
        if isinstance(request_body, str):
            try:
                request_body = json.loads(request_body)
            except json.JSONDecodeError as e:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Invalid JSON format', 'detail': str(e)})
                }
        
        # 3. 提取错误码和消息（带验证）
        error_code = request_body.get('error_code')
        error_message = request_body.get('error_message')
        
        # if not error_code or not isinstance(error_code, str):
        #     return {
        #         'statusCode': 400,
        #         'body': json.dumps({'error': 'error_code is required and must be a string'})
        #     }
        
        # 4. 写入 DynamoDB
        item = {
            'id': str(uuid.uuid4()),
            #'error_code': error_code,
            'message': error_message or 'No message provided',
            # 'timestamp': datetime.now().isoformat()
        }
        
        table.put_item(Item=item)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'success',
                'data': item  # 返回写入的数据用于验证
            })
        }
    
    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Internal server error',
                'detail': str(e)
            })
        }
