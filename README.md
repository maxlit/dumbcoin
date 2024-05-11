![demo](./gifs/240511_dumbercoin_demo.gif)

# cryptos

Bitcoin is hard to grasp since the parameters are chosen to make the coin unbreakable, however, for educational purposes we need something we can break, thus, we need a "dumber" coin, dumber than any dumbcoin you have in mind.  
Thus, let me introduce **Dumbercoin** (based on [cyclic group](https://en.wikipedia.org/wiki/Cyclic_group) `Z13`), e.g. the public key could be as simple as `(8,3)` for secret key `3`.
It makes it easier to grasp, but vulnerable, however, it still has mechanics of a coin, kind of "I'm not like them, but I can pretend".

Based on (and fork of) [karpathy/cryptos](https://github.com/karpathy/cryptos)  

If you followed [A from-scratch tour of Bitcoin in Python](http://karpathy.github.io/2021/06/21/blockchain/), look up `blog.ipynb` from this repo, I re-wrote it partly in the light of Dumbercoin.

**WARNING**: don't put any money into this coin! while some shitcoins can be relatively safe, this one isn't (not even close) by design. In plain text: *this is a damn retarded coin*!

# Differences with Bitcoin

For comparison, in bitcoin elliptic group the secret key of `3` corresponds to the public key `(112711660439710606056748659173929673102114977341539408544630613555209775888121, 25583027980570883691656905877401976406448868254816295069919888960541586679410)`, in dumbercoin this secret key corresponds to the public key `(8,3)`.


### SHA-256

repo's pure Python SHA-256 implementation closely following the [NIST FIPS 180-4](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf) spec, in `cryptos/sha256.py`. Since this is a from scratch pure Python implementation it is slow and obviously not to be used anywhere except for educational purposes. Example usage:

```bash
$ echo "some test file lol" > testfile.txt
$ shasum -a 256 testfile.txt
4a79aed64097a0cd9e87f1e88e9ad771ddb5c5d762b3c3bbf02adf3112d5d375
$ python -m cryptos.sha256 testfile.txt
4a79aed64097a0cd9e87f1e88e9ad771ddb5c5d762b3c3bbf02adf3112d5d375
```

### Keys

`getnewaddress.py` is a cli entryway to generate a new Dumcoin or Bitcoin secret/public key pair and the corresponding (base58check compressed) address.

Dumbercoin:

```bash
generated secret key:
0x3
corresponding public key:
x: 8
y: 3
compressed dmb address (b58check format):
1AjEyRmr9jrct6qQrYCEjHhZa4G8o1HBDm
```

Bitcoin:
```bash
$ python getnewaddress.py btc
generated secret key:
0xc322622e6a0033bb93ff666753f77cc8b819d274d9edea007b7e4b2af4caf025
corresponding public key:
x: 5B9D87FE091D52EA4CD49EA5CEFDD8C099DF7E6CCF510A9A94C763DE38C575D5
y: 6049637B3683076C5568EC723CF7D38FD603B88447180829BBB508C554EEA413
compressed bitcoin address (b58check format):
1DBGfUXnwTS2PRu8h3JefU9uYwYnyaTd2z
```

### Digital Signatures

Elliptic Curve Digital Signature Algorithm (ECDSA) implemented in `cryptos/ecdsa.py`, example usage:

```python
>>> from cryptos.keys import gen_key_pair
>>> from cryptos.ecdsa import sign, verify
>>> sk1, pk1 = gen_key_pair()
>>> sk2, pk2 = gen_key_pair()
>>> message = ('pk1 wants to pay pk2 1 BTC').encode('ascii')
>>> sig = sign(sk1, message)
>>> verify(pk1, message, sig)
True
>>> verify(pk2, message, sig)
False
```

### Transactions

Bitcoin transaction objects (both legacy or segwit) can be instantiated and parsed from raw bytes. An example of parsing a legacy type transaction:

```python
>>> from cryptos.transaction import Tx
>>> from io import BytesIO

>>> # example transaction in Programming Bitcoing Chapter 5
>>> raw = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
>>> tx = Tx.parse(BytesIO(raw))
>>> # we get back a Transaction object with parsed fields
>>> tx

Tx(version=1, tx_ins=[TxIn(prev_tx=b'\xd1\xc7\x89\xa9\xc6\x03\x83\xbfq_?j\xd9\xd1K\x91\xfeU\xf3\xde\xb3i\xfe]\x92\x80\xcb\x1a\x01y?\x81', prev_index=0, script_sig=3045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01 0349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a, sequence=4294967294, witness=None)], tx_outs=[TxOut(amount=32454049, script_pubkey=OP_DUP OP_HASH160 bc3b654dca7e56b04dca18f2566cdaf02e8d9ada OP_EQUALVERIFY OP_CHECKSIG), TxOut(amount=10011545, script_pubkey=OP_DUP OP_HASH160 1c4bc762dd5423e332166702cb75f40df79fea12 OP_EQUALVERIFY OP_CHECKSIG)], locktime=410393, segwit=False)
```

And we can verify that the transaction is Bitcoin law-abiding and cryptographically authentic:

```python
>>> tx.validate()
True
```

This isn't exactly a complete verification as a Bitcoin full node would do and e.g. skips verification of double spends, script sizing limits, etc., and also it only supports the (simpler) p2pkh transactions. Notably, this does not include the "modern" segwit versions used predominantly in today's Bitcoin traffic since the soft fork of BIP141 around July 2017.

### Blocks

See `cryptos/block.py` for Block class, functions and utilities.

### Lightweight Node

A lightweight Bitcoin Node that speaks a subset of the [Bitcoin protocol](https://en.bitcoin.it/wiki/Protocol_documentation) is in `cryptos/network.py`.
To the best of my knowledge, there's no node running the dumbercoin protocol.