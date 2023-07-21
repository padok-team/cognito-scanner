import boto3
import typer

from typing_extensions import Annotated

from AWSSRP import AWSSRP

cli = typer.Typer()

client_id_option = typer.Option('--client_id',help='Client ID')
region_option = typer.Option('--region',help='Region')

@cli.command(help="Get Identity Pool Keys")
def get_identity_pool_keys(
    region: Annotated[str, region_option] = 'eu-west-3',
    pool_id: Annotated[str, typer.Option('--pool_id',help='Pool ID')] = '',
    identity_pool_id: Annotated[str, typer.Option('--identity_pool_id',help='Identity pool ID')] = '',
    client_id: Annotated[str, client_id_option] = '',
    username: Annotated[str, typer.Option('--username',help='Username')] = '',
    password: Annotated[str, typer.Option('--password',help='Password')] = '',
):

    # Create SRP object
    srp = AWSSRP(
        username=username, 
        password=password, 
        pool_id=pool_id, 
        client_id=client_id, 
        pool_region=region,
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

    access_key = credentials['AccessKeyId']
    secret_key = credentials['SecretKey']
    secret_token = credentials['SessionToken']

    print('[hacker]')
    print('output = json')
    print('aws_access_key_id = %s' % access_key)
    print('aws_secret_access_key = %s' % secret_key)
    print('aws_session_token = %s' % secret_token)


@cli.command(help="Create new user account")
def account_creation(
    region: Annotated[str, region_option] = 'eu-west-3',
    user_attributes: Annotated[str, typer.Option('--user_attributes',help='User attributes (email of the user)')] = '',
    client_id: Annotated[str, client_id_option] = '',
    username: Annotated[str, typer.Option('--username',help='Username')] = '',
    password: Annotated[str, typer.Option('--password',help='Password')] = '',
):
    if not user_attributes or user_attributes == '':
        raise ValueError('You need to pass the user attributes. Type --help for more information')
    
    srp = AWSSRP(
        username=username, 
        password=password, 
        pool_id=None, 
        client_id=client_id,
        user_attributes=user_attributes,
        pool_region=region
    )

    confirmed, sub = srp.signup_user()

    print('{')
    print("\tUserConfirmed:", confirmed)
    print("\tUserSub:", sub)
    print('}')
    print("/!\ If you received a confirmation mail to sign up, you can confirm it using the confirm-sign-up")

@cli.command(help="Confirm sign up of user")
def confirm_sign_up(
    client_id: Annotated[str, client_id_option] = '',
    region: Annotated[str, region_option] = 'eu-west-3',
    username: Annotated[str, typer.Option('--username',help='Username')] = '',
    confirmation_code: Annotated[str, typer.Option('--code',help='Confirmation code')] = '',
):
    if not confirmation_code or confirmation_code == '':
        raise ValueError('Need confirmation code')
    
    srp = AWSSRP(
        username=username, 
        password=None, 
        pool_id=None, 
        client_id=client_id,
        pool_region=region
    )

    print(srp.confirm_signup(confirmation_code))


@cli.command(help="Check for existing accounts on cognito idp")
def account_oracle(
    client_id: Annotated[str, client_id_option] = '',
    region: Annotated[str, region_option] = 'eu-west-3',
):
    print('test')
    # srp = AWSSRP(
    #     username=username, 
    #     password='R4nd0mP4$$w0rd',
    #     pool_id=None, 
    #     client_id=client_id,
    #     pool_region=region
    # )

    # Pass file or only one username
    # Open file and all users
    # Test on every user
    # Make a list of the result which worked


if __name__ == "__main__":
    cli()

    


