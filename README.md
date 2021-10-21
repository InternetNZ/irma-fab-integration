![Checks](https://github.com/InternetNZ/irma-fab-integration/actions/workflows/checks.yml/badge.svg)

# IRMA FAB Integration
This repository contains FAB relying-party APIs also a CLI tool in order to work with FAB and IRMA.

## FAB Relying-Party API
The relying-party’s API is what the FAB will call when passing the credentials the end user has requested to share.
The credentials will be shared in the W3C verifiable credential format. This specification can be found
[here](https://www.w3.org/TR/vc-data-model/).

### How to run it on your local
First, make sure to create `.env` file from `.env.sample` and set the value for `SINGLE_SOURCE_API_KEY` environment
variable.

#### In a Container
You can run and manage irma backend in a container using these command:
* Create/Start your containers `docker-compose up --build -d` / `make build`
* Destroy your containers `docker-compose down` / `make down`
* Restart your containers `docker-compose restart` / `make restart`
* Stop your containers `docker-compose stop` / `make stop`
* Start your containers `docker-compose start` / `make start`

To use the local `DynamoDB`, after creating the containers run `make create-dynamodb-table` to
create the table in local DynamoDB.

#### Python Virtual Environment
This software can be run in a python virtual environment:

```
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
pip install -r requirements.dev.txt
python3 ./runserver.py
```

APIs should be accessible on http://localhost:5050

### Deployment
This a standard python WSGI app that can be deployed using standard methods. If you would like to deploy it on AWS Lambda,
it can be done by [Zappa](https://github.com/zappa/Zappa). The configuration is already provided.

To deploy using Zappa, fist make sure the requirements are installed:
```
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
pip install -r requirements.deploy.txt
```

To deploy the app:
```
zappa deploy demo
```

To update the deployed app:
```
zappa update demo
```

`NOTE:` Make sure you create the DynamoDB table `fab-vc` in your AWS account.

### FAB API endpoints
#### POST /fab/vc
This API is called by FAB platform to send back the requested VC. The received VCs
are saved in a DynamoDB table to be used later.

```
https://HOST/fab/vc'
```

A sample api call:
```
curl --request POST 'https://HOST/fab/vc' \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: API_KEY' \
  --data-raw '{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://www.fab.govt.nz/2020/credentials/v1"
  ],
  "proof": {
    "challenge": "2",
    "created": "2021-05-13 10:19:12.115119",
    "domain": "1",
    "jws": "eyJhbGciOiJSUzI1NiIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19..iYuV4ndTgQl6-2MF5QCY2iKvxdQrfVi1OvRfglSe_TfhXCUgiXhDlHCIqfDczxSWjVZTnLTL56Espsq5olEVLvOJfAn5QcB14Md164FH1palO0XR9WpdSF2io-PaVFQsZYef6TH7-Csf_v8Aoa33S7h9g2-pB7Hy8pNokfB8AeauTw89BqJseUn_RQTI0v1SHVk2B39M9g12korBO7N2krhq4FPiNv1VHPr7lfk4vP5rVadjx6mLiGo-dFI5luXmR4gky57IZhw844CBPK1p0yNwq6a32VecuW5ejHvUNO8NqPWk7h1iBI6xTVXepIWJtKi1MuTdTdKgl4jm_R3NlP6FoT7a_CA6kFdA_5deCPu2BK3eRKjiTQfA6dWaFVg5_WdEKNhHE0hPpmax7IZl9xMPIvSVPJLB0decce30yDSlSlog1q7xI688avOtNhI5_OLgeTP892U8znlyX7kp4DZlu2q44JyF4X6fQ0uryzb6DFEy-cM_BFYOgf1FITPT",
    "proofPurpose": "authentication",
    "type": "RsaSignature2018",
    "verificationMethod": "FAB_Credential_Sharing_key"
  },
  "type": "VerifiablePresentation",
  "verifiableCredential": [
    {
      "@context": [
        "https://www.w3.org/2018/credentials/v1",
        "https://www.fab.govt.nz/2020/credentials/v1"
      ],
      "credentialSubject": {
        "id": "did:pairwise:7d3725b1-365f-4b8b-bc3b-f2f508bcd7a6",
        "date-of-birth": {
          "value": "28/01/2008"
        },
        "gender": {
          "value": "Male"
        },
        "given-name": {
          "value": "John"
        },
        "surname": {
          "value": "Doe"
        },
        "proof": {
          "created": "2021-05-13 10:19:12.115084",
          "jws": "eyJhbGciOiJSUzI1NiIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19..c4l66E_Ole57aIfcFErM9yvunpfKEhNGrBc1n3hsP_XdWxvd1ut3zj2QUTKxV_k5xfGpJb3p8BnCDhsMMweh9SeGg7ZX8vJpfd2frRFciTQHQqemOw7ciiok0zt5Ex9jlAtJOXf_3S5_0WMtim9tLFnFOcEZsD44flAvODjMVlIdCX4meK_7CBYsZRvyNVHe6xTjTqq3RubyG1hDHprpTwkvUBvZKCo0B4dhmtzlnUatr_Ng9_p5AwkQu8fkzxNxoK0BJm5tOUOrOJHRBr4ikcdo5IK9xhuLhDO90xNTU7dPiA-cumxXfYAUGN9IbwmbFDXrzviZ-gY5xBS528vh4iLKdq1setlJbMNCNJhyZvSb47IEQlsfZBSi9hLQBx2pZLNlDpnaklArHxbPxXqNc7gLxsvGjrh1-CYf3VOslbdAYUYtuoNEFVnCjpJ4uicQkruSavjFB75uJUb4Mm_8L7Y_FHVrpfjbnpYoK2z4kCBEEOcdyz_KsM81Vq2FaCfi",
          "proofPurpose": "assertionMethod",
          "type": "RsaSignature2018",
          "verificationMethod": "FAB_Credential_Sharing_key"
        }
      },
      "id": "https://www.fab.govt.nz/credentials/did:idwallet:e551d834-90b0-4b8c-8c69-92c366932963",
      "issuanceDate": "2021-05-13 10:19:12.115115",
      "issuer": "https://www.fab.govt.nz",
      "type": [
        "VerifiableCredential",
        "IdentityNSNCredential"
      ]
    }
  ]
}'
```

### GET /fab/vc/\<vc_id>
This API is used to get the stored VC received from FAB.

```
https://HOST/fab/vc/<id>'
```

A sample api call:
```
curl --request GET 'https://HOST/dfab/vc/1' \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: API_KEY'
```

## CLI Tool
`./fab_irma.py` script is a tool that can be used to disclose credentials from DIA wallet (MyWai) also issuing
credentials (only NSN is supported at this stage) to IRMA wallet. You need to have DIA wallet and IRMA wallet installed
on your phone to be able to use this tool.

### Requirements
In order to be able to issue credentials to IRMA wallet, [irmago](https://github.com/privacybydesign/irmago#installing)
must be installed on your system.

Make sure you installed all the requirements as well:
```
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

### How to Run it

To get help:
```
./fab_irma.py -h
usage: fab_irma.py [-h] [-v] {fab_disclose,get_fab_disclosed_attributes,irma_issue_nsn} ...

FAB-IRMA integration tool

positional arguments:
  {fab_disclose,get_fab_disclosed_attributes,irma_issue_nsn}
                        Select one of the bellow commands
    fab_disclose        Generates FAB relying party QR code to disclose attributes.
    get_fab_disclosed_attributes
                        Returns the value of disclosed attributes.
    irma_issue_nsn      Issues given NSN to IRMA Wallet.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         More verbose
```

To disclose `nsn` credential from DIA app:
```
./fab_irma.py fab_disclose --relying-party-id 1 --relying-party-name test --attributes nsn
```

### Configuration
You can open the script with text editor and set default values for required arguments:
```
RELYING_PARTY_ID = ""
RELYING_PARTY_NAME = ""
RELYING_PARTY_LOGO = ""
RELYING_PARTY_API = ""
API_KEY = ""
IRMA_TOKEN = ""
IRMA_SERVER = ""
```
