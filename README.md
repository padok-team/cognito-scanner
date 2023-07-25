# Cognito Scanner
A simple script which implements different Cognito attacks such as Account Oracle or Priviledge Escalation

![Cover](./image/cover.png)

If you are not confortable with Cognito and want to understand the attacks better, you can check this [article](https://www.padok.fr/en/blog/aws-cognito-pentest) !

## Purpose of this repository

Cognito is a AWS service which provides a secure and scalable user authentication and access control for web and mobile applications.

This repository contains a script which implements three different attacks on Cognito :
1. Unwanted account creation
    - *What is it?* It is a malicious attempt to create user accounts without proper authorization or authentication, often leading to an influx or unauthorized accounts within a system.
    - *Parameters needed from AWS?* Only the `Client ID` protected by the Cognito instance.
2. Account Oracle
    - *What is it?* It is a type of attack where an attacker exploits an external information source (known as "oracle"), to get information about a service or to gain unauthorized access.
    - *Parameters needed from AWS?* Only the `Client ID` protected by the Cognito instance.
3. Identity pool escalation
    - *What is it?* It refers to the process where authenticated users obtain temporary credentials with higher privileges through an identity pool, allowing them to access more AWS resources than originally intended.
    - *Parameters needed from AWS?* The `Client ID`, the `Pool ID` and the `Identity Pool ID`.

## Data retrieval

To execute the attacks you will need to pass some arguments. Some of them are from AWS ressources.

#### What are these parameters?
- **Pool ID** (or User Pool ID): unique identifier assigned to a specific user pool, which is used by applications to interact with that user pool and perform authentication and user management operations.
- **Client ID**: unique identifier assigned to each application or client that integrates with a user pool, serving to authenticate and authorize requests from trusted sources during the authentication flow.
- **Identity Pool ID**: unique identifier for an identity pool, which allows authenticated users to obtain temporary AWS role and credentials for accessing authorized resources.

#### How do we get them?

You can get these parameters in multiple ways but you have to find them by yourself because it depends on the authentication implementation. They can be stored in the javascript files or in the request of the authentication page. Sometimes they are in the parameters of the request. They can also be obfuscated in the javascript code and be retrieved after deobfuscation. If you intercept the requests using Burp the parameters can also appear there.

Now that we have all the ressources needed, we can start the installation process.

## Requirements

- [Python3](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [git](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)

You can easily check that all requirements are met with the commands below:
```bash
$ python3 --version
$ pip --version
$ git --version
```

## Installation

1. Clone repository
```bash
# Using HTTPS
$ git clone https://github.com/padok-team/cognito-scanner.git
# Using SSH
$ git clone git@github.com:padok-team/cognito-scanner.git
$ cd cognito-scanner/
```
2. Create the python package
```bash
# In the root directory of your package, run the following command to build the distribution files
$ python3 setup.py sdist bdist_wheel
# Leave the directory
$ cd
# Install your package using pip
$ pip install path/to/cogniot-scanner/dist/cognito-scanner-0.1.0.tar.gz
```
3. You can now try to run the tool using `cognito-scanner --help`

## Usage

You can get details of how to use the script :
```bash
$ cognito-scanner --help
# Get information about how to use the unwanted account creation script
$ cognito-scanner account-creation --help
```

### Example

*The values here are completely faked*

#### Unwanted account creation

```bash
$ cognito-scanner account-creation --region=eu-west-3 --user_attributes=mymail@mail.com --client_id=pucXBthcyRvzwqj0WXG28DQeav --username='cognito_user' --password='R4nd0mP4$$word'
# Output
{
	UserConfirmed: False
	UserSub: 2199983e-3555-73bj-12ep-7aff05kc6kd8
}
```

#### Account Oracle

```bash
$ cognito-scanner account-oracle --client_id=pucXBthcyRvzwqj0WXG28DQeav --region=eu-west-3 --file=usernames.txt
# Output
Users found available in the file ./existing_users.txt
```

#### Identity pool escalation

```bash
$ cognito-scanner --region=eu-west-3 --pool_id=eu-west-3_liyFAGBUV --client_id=pucXBthcyRvzwqj0WXG28DQeav --identity_pool_id=eu-west-3:52983214-5fd7-438e-9088-b2e839ceefa0 --username=pentest --password='aR4ndomPassw0rd$'
# Output
[hacker]
output = json
aws_access_key_id = ROWIKQXNMUAU76LTQJEB
aws_secret_access_key = wympLAO6i9zn9GPo51hGxGRA8rsIWb8l5zzMa2iD
aws_session_token = LEGcBVDyXxpyYaVs3i0XPa2dB+dCcwbc0IAbkdVpMVf1TTBOVDrNW+P/6/PUAAZabR2SwG9r0qdq3Uj09dm4pvWh+B3BMjmkqh+6JHzj9YYxpmLPKYmLpAkHReIcr56rHLvW0mlBs/UbnthV8r1SIHzG1ze1jjCqA/mt84L8aL6KlPYJuakFWBA2f7iKO7UoR3NmHHc23N/7PfQtIexeKyKgDE1tX4OgYal1K4biAKDWeIsQm1NCfWDDB7i87kETCLYPlAuDKljfPxY1LAL0EvM9zX7lKgPUMfbtR80alEj6JhpZW/BBoEylpbfz7i3ZWSpIvqSlctqxAr5tLcYaJVjpPhP7ZhazNXriS7FZ1/Q6Uw+PGnHUxg0bk5SqjxocU/ya42X6krtJUra0R+Z9pe4dT1vKUBRBzrWyK5BdTa7gI7vOsK50jHcDLJ/CxF4JAbJrynPWTkZ/ZmHIZsD8GjEZh7Gf4fIsg3c0J1RcUevGpwFdCzq1L3rmyyD9+Esd+639u3t6lvltUZK0hPfWl7MUz4kbQ4ve1lzD3d7vn4JPydUTI/Ck34HTUSZnj834M95N6ov3jzwJevcvoCZLEaNbfyvq/UKbpBnI2OZ44kNBF5nWqDZV8BVYOxq63p1WnE++JmG2UC5Y/QZM2OqteIyFFgJ4OvaXtmY5jw6ypj8EhCZUiExl9RiDoS8X4tTlXbx4hGhpWvggKZBN+hfmZTn0FhzTjx1QWGPzVXy66D7ZvJ7O9loW9bS3ydiOfRsUg5etY/P4Ci2QomEvw/+QD4N9sFK1oHQogxq0M3lit0uUj74+Z9GnyHEcrBTKQrUo73dk5PpsENhru1bFZRromMMcB0UlmwpHcSyCq6xpf6jnYWyzfSQ/m/ZAe9UVHftOsZfblNJgftxcw4GSVX/lqpkhWi3eFpma2SvrYMckDbTWVaGmO9z+INGHqMpu7VIhNkzMNQESS
```

## Questions ?

Open an issue to contact us or to give us suggestions. We are open to collaboration !

## License

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)