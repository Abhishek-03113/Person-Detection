from flask import Flask, render_template, Response, Request, redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from ultralytics import YOLO
import cv2 as cv

# flask application configuration
app = Flask(__name__)
app.app_context().push()

# YOLO model configuration
model = YOLO("best.pt")
threshold = 0.5

# COLOR CODES BGR
green = (0, 255, 0)
red = (0, 0, 255)
blue = (255, 0, 0)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "619619"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

# LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)


# creating user databse
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))


db.create_all()


# Video Writer for YOLO
def create_video_writer(video_cap, output_filename):
    # grab the width, height, and fps of the frames in the video stream.
    frame_width = int(video_cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(video_cap.get(cv.CAP_PROP_FPS))

    # initialize the FourCC and a video writer object
    fourcc = cv.VideoWriter_fourcc(*"MP4V")
    writer = cv.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))

    return writer


# Camera and writeup setup and initialization
cap = cv.VideoCapture(0)
#writer = create_video_writer(cap, "output.mp4")


# Frame reading and model processing
def generate_frames():
    while True:
        # read the cap frame
        success, frame = cap.read()
        if not success:
            break
        else:
            detections = model(frame)[0]
            for data in detections.boxes.data.tolist():
                # extract the confidence (i.e., probability) associated with the detection
                confidence = data[4]

                # filter out weak detections by ensuring the
                # confidence is greater than the minimum confidence
                if float(confidence) < threshold:
                    continue

                # if the confidence is greater than the minimum confidence,
                # draw the bounding box on the frame
                xmin, ymin, xmax, ymax = (
                    int(data[0]),
                    int(data[1]),
                    int(data[2]),
                    int(data[3]),
                )
                cv.rectangle(frame, (xmin, ymin), (xmax, ymax), green, 2)
            #writer.write(frame)
            ret, buffer = cv.imencode(".jpg", frame)
            frame = buffer.tobytes()

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
# INITIATING LOGIN MANAGER
@login_manager.user_loader
def get(id):
    return User.query.get(id)


# Defining Routes
@app.route("/")
def index():
    return redirect("/login")


@app.route("/video")
def video():
    return render_template("index.html")


@app.route("/stream")
def stream():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/login", methods=["GET"])
def get_login():
    return render_template("login.html")


@app.route("/signup", methods=["GET"])
def get_signup():
    return render_template("signup.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = User.query.filter_by(email=email).first()
    login_user(user)
    return redirect("/video")


@app.route("/signup", methods=["POST"])
def signup_post():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(email=email).first()
    login_user(user)
    return redirect("/login")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=False)
