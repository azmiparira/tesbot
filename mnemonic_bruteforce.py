
from itertools import product
from mnemonic import Mnemonic
from bip32utils import BIP32Key
import hashlib

# Target Ethereum address
TARGET_ADDRESS = "0xdef2d580a0f329db1b6068fdaf224814993e9c41".lower()

# BIP39 wordlist
mnemo = Mnemonic("english")
wordlist = mnemo.wordlist

# Base mnemonic with missing words at index 0 and 9
base_mnemonic = [
    "",         # Word 1 - to be guessed
    "escape",
    "repair",
    "rain",
    "party",
    "nominee",
    "eager",
    "alien",
    "exchange",
    "",         # Word 10 - to be guessed
    "kidney",
    "finish"
]

def mnemonic_to_eth_address(mnemonic_phrase):
    seed = mnemo.to_seed(mnemonic_phrase, passphrase="")
    master_key = BIP32Key.fromEntropy(seed)
    purpose_key = master_key.ChildKey(44 + BIP32Key.HARDEN)
    coin_type_key = purpose_key.ChildKey(60 + BIP32Key.HARDEN)
    account_key = coin_type_key.ChildKey(0 + BIP32Key.HARDEN)
    change_key = account_key.ChildKey(0)
    address_key = change_key.ChildKey(0)
    pubkey = address_key.PublicKey()
    keccak_hash = hashlib.new("keccak256")
    keccak_hash.update(pubkey[1:])
    return "0x" + keccak_hash.hexdigest()[-40:]

def main():
    attempts = 0
    for w1, w10 in product(wordlist, repeat=2):
        mnemonic = base_mnemonic[:]
        mnemonic[0] = w1
        mnemonic[9] = w10
        phrase = " ".join(mnemonic)
        try:
            address = mnemonic_to_eth_address(phrase)
            if address == TARGET_ADDRESS:
                print(f"✅ FOUND!")
                print(f"Word 1 : {w1}")
                print(f"Word 10: {w10}")
                print(f"Mnemonic: {phrase}")
                return
        except Exception as e:
            continue
        attempts += 1
        if attempts % 50000 == 0:
            print(f"Checked {attempts} combinations...")

    print("❌ No matching combination found.")

if __name__ == "__main__":
    main()
