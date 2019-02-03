from flask import Flask, render_template, Response
from camera import VideoCamera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    camera = VideoCamera()
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/admin/')
def admin():
    return render_template('admin/index.html')

@app.route('/admin/illAct/')
def cheaters():
    return render_template('admin/illAct/index.html')

@app.route('/admin/nonCafe/')
def nonCafe():
    return render_template('admin/nonCafe/index.html')

@app.route('/admin/todayAct/')
def toDayAct():
    return render_template('admin/todayAct/index.html')

@app.route('/admin/userStat/')
def userStat():
    return render_template('admin/userStat/index.html')

@app.route('/admin/regUser/')
def regUser():
    return render_template('admin/regUser/index.html')

if __name__ == '__main__':
    app.run()