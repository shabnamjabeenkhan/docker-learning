from flask import Flask
import redis
import os

r = redis.Redis(host="redisDatabase4", port=6379)
app =Flask(__name__)
@app.route("/")
def welcome():
    return "Welcome!"

@app.route("/count")
def visit():
    return "Count Page"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)    