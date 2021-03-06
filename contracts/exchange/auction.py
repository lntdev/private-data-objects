# Copyright 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import shlex
import logging

logger = logging.getLogger(__name__)

from pdo.client.SchemeExpression import SchemeExpression
from pdo.client.controller.commands.send import send_to_contract

## -----------------------------------------------------------------
## -----------------------------------------------------------------
def __command_auction__(state, bindings, pargs) :
    """controller command to interact with an auction contract
    """

    parser = argparse.ArgumentParser(prog='auction')
    parser.add_argument('-e', '--enclave', help='URL of the enclave service to use', type=str)
    parser.add_argument('-f', '--save_file', help='File where contract data is stored', type=str)
    parser.add_argument('-q', '--quiet', help='Suppress printing the result', action='store_true')
    parser.add_argument('-w', '--wait', help='Wait for the transaction to commit', action='store_true')

    subparsers = parser.add_subparsers(dest='command')

    subparser = subparsers.add_parser('get_verifying_key')
    subparser.add_argument('-s', '--symbol', help='binding symbol for result', type=str)

    subparser = subparsers.add_parser('get_offered_asset')
    subparser = subparsers.add_parser('get_requested_asset')

    subparser = subparsers.add_parser('initialize')
    subparser.add_argument('-r', '--root', help='key for the root authority for requested issuer', type=str, required=True)
    subparser.add_argument('-t', '--type_id', help='contract identifier for the requested asset type', type=str, required=True)
    subparser.add_argument('-o', '--owner', help='identity of the asset owner; ECDSA key', type=str, default="")
    subparser.add_argument('-c', '--count', help='amount requested', type=int, required=True)

    subparser = subparsers.add_parser('offer')
    subparser.add_argument('-a', '--asset', help='serialized escrowed asset', type=str, required=True)

    subparser = subparsers.add_parser('claim_offer')
    subparser.add_argument('-s', '--symbol', help='binding symbol for result', type=str)

    subparser = subparsers.add_parser('cancel_auction')
    subparser.add_argument('-s', '--symbol', help='binding symbol for result', type=str)

    subparser = subparsers.add_parser('close_auction')
    subparser = subparsers.add_parser('confirm_close')

    subparser = subparsers.add_parser('submit_bid')
    subparser.add_argument('-a', '--asset', help='serialized escrowed asset', type=str, required=True)

    subparser = subparsers.add_parser('claim_bid')
    subparser.add_argument('-s', '--symbol', help='binding symbol for result', type=str)

    subparser = subparsers.add_parser('max_bid')
    subparser = subparsers.add_parser('check_bid')

    subparser = subparsers.add_parser('cancel_bid')
    subparser.add_argument('-s', '--symbol', help='binding symbol for result', type=str)

    options = parser.parse_args(pargs)

    extraparams={'quiet' : options.quiet, 'wait' : options.wait}

    # -------------------------------------------------------
    if options.command == 'get_verifying_key' :
        extraparams['commit'] = False
        message = "'(get-verifying-key)"
        result = send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
        if result and options.symbol :
            bindings.bind(options.symbol, result)
        return

    # -------------------------------------------------------
    if options.command == 'get_offered_asset' :
        extraparams['commit'] = False
        message = "'(examine-offered-asset)"
        result = send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
        return

    # -------------------------------------------------------
    if options.command == 'get_requested_asset' :
        extraparams['commit'] = False
        message = "'(examine-requested-asset)"
        result = send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
        return

    # -------------------------------------------------------
    if options.command == 'initialize' :
        asset_request = "(\"{0}\" {1} \"{2}\")".format(options.type_id, options.count, options.owner)
        message = "'(initialize {0} \"{1}\")".format(asset_request, options.root)
        result = send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
        return

    # -------------------------------------------------------
    if options.command == 'offer' :
        message = "'(offer-asset {0})".format(options.asset)
        result = send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
        return

    # -------------------------------------------------------
    if options.command == 'claim_offer' :
        extraparams['commit'] = False
        message = "'(claim-offer)"
        result = send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
        if result and options.symbol :
            bindings.bind(options.symbol, result)
        return

    # -------------------------------------------------------
    if options.command == 'cancel_auction' :
        message = "'(cancel-auction)"
        result = send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
        if result == "#t" :
            extraparams['commit'] = False
            message = "'(cancel-auction-attestation)"
            send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
            if result and options.symbol :
                bindings.bind(options.symbol, result)
        return

    # -------------------------------------------------------
    if options.command == 'close_auction' :
        message = "'(close-auction)"
        send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
        return

    # -------------------------------------------------------
    if options.command == 'confirm_close' :
        message = "'(confirm-close)"
        send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
        return

    # -------------------------------------------------------
    if options.command == 'submit_bid' :
        message = "'(submit-bid {0})".format(options.asset)
        result = send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
        return

    # -------------------------------------------------------
    if options.command == 'max_bid' :
        extraparams['commit'] = False
        message = "'(max-bid)"
        send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
        return

    # -------------------------------------------------------
    if options.command == 'check_bid' :
        extraparams['commit'] = False
        message = "'(check-bid)"
        send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
        return

    # -------------------------------------------------------
    if options.command == 'claim_bid' :
        extraparams['commit'] = False
        message = "'(claim-bid)"
        result = send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
        if result and options.symbol :
            bindings.bind(options.symbol, result)
        return

    # -------------------------------------------------------
    if options.command == 'cancel_bid' :
        message = "'(cancel-bid)"
        result = send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
        if result == "#t" :
            extraparams['commit'] = False
            message = "'(cancel-bid-attestation)"
            result = send_to_contract(state, options.save_file, options.enclave, message, **extraparams)
            if result and options.symbol :
                bindings.bind(options.symbol, result)

        return

## -----------------------------------------------------------------
## -----------------------------------------------------------------
def do_auction(self, args) :
    """
    auction -- invoke methods from the auction contract
    """

    pargs = shlex.split(self.bindings.expand(args))

    try :
        __command_auction__(self.state, self.bindings, pargs)

    except SystemExit as se :
        if se.code > 0 : print('An error occurred processing {0}: {1}'.format(args, str(se)))
        return

    except Exception as e :
        print('An error occurred processing {0}: {1}'.format(args, str(e)))
        return

## -----------------------------------------------------------------
## -----------------------------------------------------------------
def load_commands(cmdclass) :
    setattr(cmdclass, 'do_auction', do_auction)
