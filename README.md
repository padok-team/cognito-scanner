# cognito-scanner
A simple script which implements different Cognito attacks such as Account Oracle or Priviledge Escalation

## Purpose of this repository

Cognito is a AWS tool which provides a secure and scalable user authentication and access control service for web and mobile applications.

This repository contains a script which implements three different attacks on Cognito :
1. Unwanted account creation
2. Account Oracle
3. Identity pool escalation

## Requirements

- [Python3](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [git](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)

You can easily check that all requirements are met with the commands below:
```bash
$ python3 --version
$ pip3 --version
$ git --version
```

## Installation

1. Clone repository
```bash
# Using HTTPS
$ git clone https://github.com/padok-team/cognito-scanner.git
# Using SSH
$ git@github.com:padok-team/cognito-scanner.git
$ cd cognito-scanner/
```
2. [Optionnal] Create a python virtual environment
```bash
# Create the environment
$ python3 -m venv <env_name>
# Activate it
$ source <env_name>/bin/activate
```
3. Install the necessary packages `pip install requirements.txt`

## Usage

You can get details of how to use the script :
```bash
$ python3 cognito-scanner.py --help
# Get information about how to use the unwanted account creation script
$ python3 cognito-scanner.py account-creation --help
```

### Example

*The values here are completely faked*

#### Unwanted account creation

```bash
$ python3 cognito-scanner.py account-creation --region=eu-west-3 --user_attributes=mymail@mail.com --client_id=pucXBthcyRvzwqj0WXG28DQeav --username='cognito_user' --password='R4nd0mP4$$word'
# Output
{
	UserConfirmed: False
	UserSub: 2199983e-3555-73bj-12ep-7aff05kc6kd8
}
```

#### Account Oracle

```bash
$ python3 cognito-scanner.py account-oracle --client_id=pucXBthcyRvzwqj0WXG28DQeav --region=eu-west-3 --file=usernames.txt
# Output
Users found available in the file ./existing_users.txt
```

#### Identity pool escalation

```bash
$ python3 cognito-scanner.py --region=eu-west-3 --pool_id=eu-west-3_liyFAGBUV --client_id=pucXBthcyRvzwqj0WXG28DQeav --identity_pool_id=eu-west-3:52983214-5fd7-438e-9088-b2e839ceefa0 --username=pentest --password='aR4ndomPassw0rd$' --user-attributes Name=email,Value=pentest@h4x0r.com
```

## Questions ?

Open an issue to contact us or to give us suggestions. We are open to collaboration !

## License