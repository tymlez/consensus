from bigchaindb.consensus import BaseConsensusRules

from bigchaindb.common import exceptions

import urllib.request, urllib.parse, urllib.error

import os

from bigchaindb.common.exceptions import (KeypairMismatchException,
                                          InvalidHash, InvalidSignature,
                                          AmountError, AssetIdMismatch)

# Unbound super requires both arguments to get the correct behavior with
# staticmethods
def sup():
    return super(ConsensusRulesTemplate,
                 ConsensusRulesTemplate)

class ConsensusRulesTemplate(BaseConsensusRules):

    @staticmethod
    def validate_transaction(bigchain, transaction):
        """Validate a transaction.

        Args:
            bigchain (Bigchain): an instantiated ``bigchaindb.Bigchain`` object.
            transaction (dict): transaction to validate.

        Returns:
            The transaction if the transaction is valid else it raises an
            exception describing the reason why the transaction is invalid.

        Raises:
            Descriptive exceptions indicating the reason the transaction failed.
            See the `exceptions` module for bigchain-native error classes.
        """

        tx = transaction.to_dict();

        print ("Validate_transaction * :", tx['id']);

        details = urllib.parse.urlencode(transaction.to_dict());
        details = details.encode('UTF-8')

        ip = 'http://' + os.environ['HOST_IP'] + ':7070';

        url = urllib.request.Request(ip, details)
        url.add_header("User-Agent","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13")

        responseData = urllib.request.urlopen(url).read().decode('utf8', 'ignore')

        print ("JS answer:", responseData);

        if responseData == "FAIL":
            raise InvalidHash('Consensus plugin error, not a hash.');

        if responseData == "ALLOW":
            return True;

        if responseData == "NEXT":
            return transaction.validate(bigchain);


    @staticmethod
    def validate_block(bigchain, block):
        """Validate a block.

        Args:
            bigchain (Bigchain): an instantiated ``bigchaindb.Bigchain`` object.
            block (dict): block to validate.

        Returns:
            The block if the block is valid else it raises an exception
            describing the reason why the block is invalid.

        Raises:
            Descriptive exceptions indicating the reason the block failed.
            See the `exceptions` module for bigchain-native error classes.
        """

        blockDict = block.to_dict();

        print ("Validate_ Block ******************************************* ", blockDict['id']);

        details = urllib.parse.urlencode(blockDict)
        details = details.encode('UTF-8')
        url = urllib.request.Request('http://172.17.0.1:7071', details)
        url.add_header("User-Agent","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13")

        responseData = urllib.request.urlopen(url).read().decode('utf8', 'ignore')

        print ("JS answer for block:", responseData);

        if responseData != "OK":
          raise exceptions.OperationError('consensus.js return FAIL')


        print ("BLOCK is OK");

        #return sup().validate_block(bigchain, block)
        return block.validate(bigchain)

    @staticmethod
    def create_transaction(*args, **kwargs):
        """Create a new transaction.
        Args:
            The signature of this method is left to plugin authors to decide.
        Returns:
            dict: newly constructed transaction.
        """
        print("Hey! You're using create_transaction from your own consensus "
              "rules now!")
        return sup().create_transaction(*args, **kwargs)

    @staticmethod
    def sign_transaction(transaction, *args, **kwargs):
        """Sign a transaction.
        Args:
            transaction (dict): transaction to sign.
            any other arguments are left to plugin authors to decide.
        Returns:
            dict: transaction with any signatures applied.
        """
        print("Hey! You're using sign_transaction from your own consensus "
              "rules now!")
        return sup().sign_transaction(transaction, *args, **kwargs)

    @staticmethod
    def verify_signature(signed_transaction):
        """Verify the signature of a transaction.
        Args:
            signed_transaction (dict): signed transaction to verify
        Returns:
            bool: True if the transaction's required signature data is present
                and correct, False otherwise.
        """
        print("Hey! You're using validate_signature from your own consensus "
              "rules now!")
        return sup().verify_signature(signed_transaction)
