import boto3

REGION_NAME = 'us-east-1'
CLIENT_ID = '4gg2css4mvsjoca6s44oe54b7p'

client = boto3.client('cognito-idp', region_name=REGION_NAME)

def register_user(username, password, email):
    try:
        response = client.sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
            ]
        )
        return {"success": True, "response": response}
    except client.exceptions.ClientError as e:
        return {"success": False, "error": str(e)}

def login_user(username, password):
    try:
        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        return {"success": True, "response": response}
    except client.exceptions.ClientError as e:
        return {"success": False, "error": str(e)}