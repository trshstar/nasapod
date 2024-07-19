from nasa import apod
import datetime
import random
from flask import Flask, render_template, url_for, request, redirect

#A web application that generates a random image from the NASA APOD API

minDate = datetime.datetime(1995, 6, 16)
minDateApod = str(minDate.year) + "-" + str(minDate.month) + "-" + str(minDate.day)
minDateUpdated = minDate.strftime("%x")
maxDate = datetime.datetime.now()
maxDateApod = str(maxDate.year) + "-" + str(maxDate.month) + "-" + str(maxDate.day)
maxDateUpdated = maxDate.strftime("%x")


def random_date(start, end):
    #Generate a random datetime between `start` and `end`.

    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + datetime.timedelta(seconds=random_seconds)


app = Flask(__name__)


@app.route("/")
def index():
    todayPicture = apod.apod(maxDateApod)
    todayTitle = todayPicture.title
    return render_template("index.html", image_url=todayPicture.url, image_date=maxDateUpdated, image_title=todayTitle)


@app.route("/handle_button", methods=['POST'])
def handle_button():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'button_clicked':
            randDate = random_date(minDate, maxDate)
            randDateApod = randDate.strftime('%Y-%m-%d')
            randDateUpdated = randDate.strftime('%x')
            randPicture = apod.apod(randDateApod)
        return render_template("index.html", image_url=randPicture.url, image_date=randDateUpdated,
                               image_title=randPicture.title)
    return redirect("/")

@app.route("/submit", methods=['POST'])
def submit():
    if request.method == 'POST':
        date = request.form['requestedDate']
        pic = apod.apod(date)
        dateUpdated = date[8:11] + "/" + date[5:7] + "/" + date[0:4]
        return render_template("index.html", image_url=pic.url, image_date=dateUpdated, image_title=pic.title)

if __name__ == "__main__":
    app.run(debug=True)
