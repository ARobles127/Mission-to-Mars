from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Set up scraping route
@app.route("/scraping")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   # Update database
   mars.update_one({},{"$set": mars_data}, upsert=True)
   # Redirect after scraping the data
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()