# AirStrike Stage0

This project is a Stage0 C2 that is highly customizable and can be used to create a template for your own C2 or to use it as a base for your own C2 agents.

Currently there are 4 different parts to this project

1. `agent` is a folder which has two different agents, one is written in C while the other is written in Rust. the code is most likely not perfect and is only to be used as a template to explain the life cycle of a C2 agent.

2. `backend` is the python(Flask) backend server which handles communications between the frontned and all the agents, It will bind to port 23000 on localhost only by default, you need to write your own reverse proxy on nginx or apache to access it from the internet.

3. `frontend` is a web application written in ReactJS that connects to the backend server, It's also dockerized and can be used to serve the frontend application on port 23001 on localhost only by default, you need to write your own reverse proxy on nginx or apache to access it from the internet. (I don't recommend access to the backend server from the internet instead use SSH tunneling)

4. `demo` is a python test script to see if any changes break the backend without having to spawn a new shell everytime.

---

To start the backend and frontend server just make sure you have docker and docker-compose installed and run `docker-compose up -d` in the root folder of the project, you can also run `docker-compose down` to stop the containers.

---

I hope this project helps you to create your own C2 agents and backend servers, if you have any questions or suggestions please reach out to me on twitter at [https://www.twitter.com/q8fawazo]
