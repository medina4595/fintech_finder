import os
import requests
from dotenv import load_dotenv
load_dotenv()
from bip44 import Wallet
from web3 import Account
from web3.auto.infura.kovan import w3
from web3 import middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

def generate_account():
    """Create a digital wallet and Ethereum account from a mnemonic seed phrase."""
    mnemonic = os.getenv("MNEMONIC")

    wallet = Wallet(mnemonic)

    private, public = wallet.derive_account("eth")

    account = Account.privateKeyToAccount(private)

    return account

def get_balance(address):
    """Using an Ethereum account address access the balance of Ether"""
    wei_balance = w3.eth.get_balance(address)

    ether = w3.fromWei(wei_balance, "ether")

    return ether


def send_transaction(account, to, wage):
    """Send an authorized transaction to the Kovan testnet."""
    w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

    value = w3.toWei(wage, "ether")

    gasEstimate = w3.eth.estimateGas({"to": to, "from": account.address, "value": value})

    raw_tx = {
        "to": to,
        "from": account.address,
        "value": value,
        "gas": gasEstimate,
        "gasPrice": w3.eth.generateGasPrice(),
        "nonce": w3.eth.getTransactionCount(account.address)
    }

    signed_tx = account.signTransaction(raw_tx)

    return w3.eth.sendRawTransaction(signed_tx.rawTransaction)
