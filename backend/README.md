# AirStrike backend

The backend is running with flask / sqlalchemy & socket.io

To start the server just make a virtualenv first

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 app.py
```

You can also clean up the folder shellcode and the database whenever you are running the server again

```bash
rm -rf shellcode/*
rm -rf database.sqlite
```

---

You can change what kind of information you are expecting from the agent in the `models.py`, for example your agent doesn't send a username, you can just remove it from there

---

You can also change the way you authenticate a valid agent from a random http connection in the `custom.py` function `FindSession` where you can specifiy if you want to use headers/cookies/postdata etc and change the type of encryption used, XOR/Base64 in my case

---

The file structure is fairly simple and you can change lots of stuff to suite your needs
