from flask import Flask,request,render_template_string
import time

app=Flask(__name__)
app.secret_key="mysecret"

USERNAME="admin"
PASSWORD="vasanth"

ip_data={}

DELAY_SECONDS=180
MAX_ATTEMPTS=5
MAX_ROUNDS=3

def get_ip_data(ip):
    if ip not in ip_data:
        ip_data[ip]={
            "attempts":0,
            "rounds":0,
            "locked_until":0,
            "logs":[]
        }
    return ip_data[ip]

@app.route("/",methods=["GET","POST"])
def login():
    message=""
    color="red"
    show_cm=False
    locked=False
    waiting=False
    wait_sec=0
    ip=request.headers.get('X-Forwarded-For',request.remote_addr)
    if ',' in ip:
        ip=ip.split(',')[0].strip()
    d=get_ip_data(ip)

    if d["rounds"]>=MAX_ROUNDS:
        return render_template_string(
            open("login.html",encoding="utf-8").read(),
            message="🚫 IP Permanently Locked!",
            color="red",locked=True,waiting=False,
            wait_sec=0,logs=d["logs"],show_cm=False
        )

    now=time.time()
    if d["locked_until"]>now:
        wait_sec=int(d["locked_until"]-now)
        return render_template_string(
            open("login.html",encoding="utf-8").read(),
            message=f"⏳ Wait {wait_sec} seconds!",
            color="orange",locked=False,waiting=True,
            wait_sec=wait_sec,logs=d["logs"],show_cm=False
        )
    elif d["locked_until"]!=0 and d["locked_until"]<=now:
        d["attempts"]=0
        d["locked_until"]=0

    if request.method=="POST":
        user=request.form["username"]
        pwd=request.form["password"]

        if user==USERNAME and pwd==PASSWORD:
            d["attempts"]=0
            d["rounds"]=0
            d["locked_until"]=0
            message= "✅ Login Successful! Welcome "+user
            color="green"
            show_cm=True
            d["logs"].append({"result": "SUCCESS"})

        else:
            d["attempts"]+=1
            left=MAX_ATTEMPTS-d["attempts"]
            d["logs"].append({"result":"FAILED"})

            if d["attempts"]>=MAX_ATTEMPTS:
                d["rounds"]+=1

                if d["rounds"]>=MAX_ROUNDS:
                    locked=True
                    message="🚫 IP Permanently Locked!"
                    color="red"
                else:
                    d["locked_until"]=time.time()+DELAY_SECONDS
                    wait_sec=DELAY_SECONDS
                    waiting=True
                    message=f"⏳ Round {d['rounds']}/{MAX_ROUNDS-1} done! Wait 3 minutes!"
                    color="orange"
            else:
                message=f"❌ Wrong! {left} attempts left!"
                color="red"

    return render_template_string(
        open("login.html",encoding="utf-8").read(),
        message=message,color=color,
        locked=locked,waiting=waiting,
        wait_sec=wait_sec,logs=d["logs"],
        show_cm=show_cm
    )

import os
port=int(os.environ.get("PORT",5000))
app.run(host="0.0.0.0",port=port)
