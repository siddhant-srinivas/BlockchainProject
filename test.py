import hashlib
import hmac
import random



# Function to create a response using HMAC
def create_response(challenge, bit, secret_key):
    
    hmac_digest = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()  # Compute HMAC
    return hmac_digest

# Function to verify the response
def verify_response(challenge, bit, response, secret_key):
    expected_response = create_response(challenge, bit, secret_key)
    return hmac.compare_digest(expected_response, response)


secret_key = "supersecretkey"
challenge = ''.join(random.choices('0123456789abcdef', k=16))
bit = random.randint(0, 1)
message = challenge + str(bit)  # Concatenate challenge and bit
response = create_response(challenge, bit, secret_key)
is_authenticated = verify_response(challenge, bit, response, secret_key)

if is_authenticated:
    print("Authentication successful!")
else:
    print("Authentication failed!")
