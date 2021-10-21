#!/usr/bin/env python3
import argparse
import json
import datetime
import time
import logging

import qrcode
import requests
import subprocess

RELYING_PARTY_ID = ""
RELYING_PARTY_NAME = ""
RELYING_PARTY_LOGO = ""
API_KEY = ""
IRMA_TOKEN = "secret-fake-token"
IRMA_SERVER = "https://pnonvsmdy9.execute-api.ap-southeast-2.amazonaws.com/dev"

FAB_IDENTITY_CREDENTIAL = 'identity'
FAB_IDENTITY_ATTRIBUTES = [
    'given_names', 'surname', 'date-of-birth', 'gender'
]

# Config logger
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def fab_disclose(args):
    qr = qrcode.QRCode()

    relying_party_data = {
        "relyingPartyLogo": args.relying_party_logo,
        "relyingPartyId": args.relying_party_id,
        "relyingPartySessionId": args.session_id,
        "relyingPartyName": args.relying_party_name,
        "purpose": args.purpose,
        "attributesToSend": args.attributes
    }

    qrcode_data = json.dumps(relying_party_data, indent=None)

    qr.add_data(qrcode_data)
    qr.print_ascii()

    LOGGER.info("Session ID: %s", args.session_id)

    for i in range(10):
        LOGGER.debug("Checking for response ...")
        response = _fetch_fab_disclosed_attributes(args.session_id)

        if response.status_code == requests.codes.no_content:
            time.sleep(2)
            continue

        if response.status_code == requests.codes.ok:
            break

        response.raise_for_status()
    else:
        LOGGER.warning("Did not receive the disclosed VC! Please try again.")
        exit(1)

    LOGGER.debug("Disclosed VC from FAB: %s", response.json())
    _extract_attributes(response)


def _fetch_fab_disclosed_attributes(session_id):
    response = requests.get(
        url=f"https://f9emnttxd6.execute-api.ap-southeast-2.amazonaws.com/demo/fab/vc/{session_id}",
        headers={
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
            "origin": "http://localhost:8000"
        }
    )

    return response


def _extract_attributes(response):
    disclosed_attributes = response.json()['verifiableCredential'][0]['credentialSubject']
    for attribute in args.attributes:
        if attribute == FAB_IDENTITY_CREDENTIAL:
            print(str.upper(FAB_IDENTITY_CREDENTIAL))
            for id_attribute in FAB_IDENTITY_ATTRIBUTES:
                print("  {} : {}".format(str.upper(id_attribute), disclosed_attributes[id_attribute]['value']))
        else:
            print("{} : {}".format(str.upper(attribute), disclosed_attributes[attribute]['value']))


def get_fab_disclosed_attributes(args):
    response = _fetch_fab_disclosed_attributes(args.session_id)

    if response.status_code != requests.codes.ok:
        response.raise_for_status()

    _extract_attributes(response)


def irma_issue_nsn(args):
    irma_command = ['irma', 'session', '--server', IRMA_SERVER,
                    '-a', 'token', '--key', IRMA_TOKEN, '--issue',
                    'irma-demo.inz-nsn.nsn={}'.format(args.nsn)]

    if args.verbose:
        irma_command.append('-vv')

    result = subprocess.run(irma_command, timeout=60)

    result.check_returncode()


if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(
        description='FAB-IRMA integration tool'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        default=False,
        action='store_true',
        help='More verbose'
    )

    subparsers = parser.add_subparsers(help='Select one of the bellow commands')

    parser_fab_disclose = subparsers.add_parser(
        'fab_disclose',
        help='Generates FAB relying party QR code to disclose attributes.'
    )
    parser_fab_disclose.add_argument(
        '--relying-party-id',
        nargs='?',
        required=True,
        default=RELYING_PARTY_ID,
        help='Relying party ID'
    )

    parser_fab_disclose.add_argument(
        '--relying-party-name',
        nargs='?',
        required=True,
        default=RELYING_PARTY_NAME,
        help='Relying party name'
    )

    parser_fab_disclose.add_argument(
        '--relying-party-logo',
        nargs='?',
        default=RELYING_PARTY_LOGO,
        help='Relying party name'
    )

    parser_fab_disclose.add_argument(
        '--session-id',
        nargs='?',
        default=datetime.datetime.now().strftime('%s'),
        help='Session ID. Default epoch'
    )

    parser_fab_disclose.add_argument(
        '--purpose',
        nargs='?',
        default="Testing FAB-IRMA integration",
        help='Purpose of requesting the attributes'
    )

    parser_fab_disclose.add_argument(
        '--attributes',
        nargs='*',
        default=['nsn'],
        choices=['nsn', 'email', 'photo', 'identity'],
        help='Attributes to be disclosed. Default `NSN`'
    )

    parser_fab_disclose.set_defaults(func=fab_disclose)

    parser_get_disclosed_attributes = subparsers.add_parser(
        'get_fab_disclosed_attributes',
        help='Returns the value of disclosed attributes.'
    )

    parser_get_disclosed_attributes.add_argument(
        'session_id',
        help='Session ID'
    )

    parser_get_disclosed_attributes.add_argument(
        '--attributes',
        nargs='*',
        default=['nsn'],
        help='Attributes to be disclosed. Default `NSN`'
    )

    parser_get_disclosed_attributes.set_defaults(func=get_fab_disclosed_attributes)

    parser_irma_issue_nsn = subparsers.add_parser(
        'irma_issue_nsn',
        help='Issues given NSN to IRMA Wallet.'
    )

    parser_irma_issue_nsn.add_argument(
        'nsn',
        help='National Student Number'
    )

    parser_irma_issue_nsn.set_defaults(func=irma_issue_nsn)

    args = parser.parse_args()

    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)

    try:
        args.func(args)
    except AttributeError as err:
        parser.print_help()
