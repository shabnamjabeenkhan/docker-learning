from flask import Flask, render_template
import redis
import os


redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=redis_host, port=redis_port)
app =Flask(__name__)
@app.route("/")
def welcome():
    return render_template(
        "index.html",
        title="CoderCo Challenge",
        message="Welcome to VisitTracker Pro by CoderCo!",
        paragraph="Click the button below to view the number of times this page has been visited.",
        button_text="View Visit Count",
    )

@app.route("/count")
def visit():
   visit_count = r.incr("visits")
   return render_template("count.html", visit_count=visit_count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)    