from flask import Flask
import redis
import os


redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=redis_host, port=redis_port)
app =Flask(__name__)
@app.route("/")
def welcome():
    return "Welcome to the CoderCo Challenge!"

@app.route("/count")
def visit():
   visit_count = r.incr("visits")
   return f"This page has been visited {visit_count} times!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)    