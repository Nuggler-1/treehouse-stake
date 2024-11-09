from utils.utils import send_tx, wait_for_gas, error_handler
from utils.constants import DEPOSIT_CONTRACT, PRIVATE_KEYS, logo 
from config import *

from web3 import Web3 
from loguru import logger 

import random
import time
@error_handler('deposit')
def deposit(web3,account): 

    tx = {
        'to': DEPOSIT_CONTRACT,
        'from': account.address,
        'data': '0xf6326fb3'
    }
    
    rounding_min = len( str(AMOUNT_TO_DEPOSIT[0]).split('.')[1] )
    rounding_max = rounding_min + 2
    rounding = random.randint(rounding_min, rounding_max)
    amount = round(random.uniform(*AMOUNT_TO_DEPOSIT), rounding)
    logger.info(f'{account.address}: depositing {amount} ETH')
    amount = Web3.to_wei(amount, 'ether')

    return send_tx(web3, account, tx, value=amount)

def main(): 

    with open(PRIVATE_KEYS, 'r', encoding='utf-8') as file: 
        private_keys = file.read().splitlines()

    if RANDOMIZE_ACCOUNTS: 
        random.shuffle(private_keys)

    web3 = Web3(Web3.HTTPProvider(RPC))

    for private_key in private_keys: 
        account = web3.eth.account.from_key(private_key)
        wait_for_gas(web3)
        deposit(web3,account)
        time.sleep(random.uniform(*SLEEP))

if __name__ == '__main__': 
    logger.opt(raw=True).info(logo)
    print('\n\n')
    main()

