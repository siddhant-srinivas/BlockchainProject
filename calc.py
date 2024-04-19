import hashlib
import hmac
import random


challenge = input("Enter the challenge: ")
bit = input("Enter the bit: ")
secretkey = input("Enter the secretkey: ")
challenge = challenge + str(bit)
answer = hmac.new(secretkey.encode(), challenge.encode(), hashlib.sha256).hexdigest()
print('The response should be : ', answer)