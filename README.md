# AirStrike Stage0

There are 4 different folder

1. `agent` is a example C agent that can be used with the C2.
2. `backend` is the python(Flask) backend server which handles communications between the frontned and all the agents.
3. `frontend` is a web application written in ReactJS that connects to the backend server, You don't have to compile it as there is a build version ready, you just need to serve it via `python -m http.server` or something similar.
4. `demo` is a python test script to see if any changes break the backend without having to spawn a new shell everytime.

---

This was written by Fawaz, you can find me at [https://www.twitter.com/q8fawazo]
