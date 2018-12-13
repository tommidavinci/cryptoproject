import nacl.encoding
import nacl.signing
import nacl.secret
import nacl.utils
from nacl.public import PrivateKey, Box, PublicKey


skserver = PrivateKey.generate()
# Generate a new random signing key
signing_key = nacl.signing.SigningKey(bytes(skserver))

# Sign a message with the signing key
signed = signing_key.sign(b"Attack at Dawn")

# Obtain the verify key for a given signing key
verify_key = signing_key.verify_key

# Serialize the verify key to send it to a third party
verify_key_hex = verify_key.encode(encoder=nacl.encoding.HexEncoder)
print(verify_key)
print(verify_key_hex)
# Create a VerifyKey object from a hex serialized public key
verify_key = nacl.signing.VerifyKey(verify_key_hex,encoder=nacl.encoding.HexEncoder)

# Check the validity of a message's signature
# The message and the signature can either be passed separately or
# concatenated together.  These are equivalent:
verify_key.verify(signed)
verify_key.verify(signed.message, signed.signature)

print(verify_key.verify(signed))