# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template
from flask import request, url_for, redirect, flash ,jsonify

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, '../FSGAN/fsgan/docs'),
    SECRET_KEY = 'dev',
    SOURCE=None,
    TARGET=None,
)

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        ts=request.form.get('ts')
        file=request.files.get('file')
        file.save(os.path.join(app.config['UPLOADED_PATH'], file.filename))
        print(app.config['UPLOADED_PATH'])
        
        if ts == 'source':
            app.config["SOURCE"]=os.path.join(app.config['UPLOADED_PATH'], file.filename)
        else:
            app.config["TARGET"]=os.path.join(app.config['UPLOADED_PATH'], file.filename)
        if(app.config["SOURCE"]!=None and app.config["TARGET"]!=None):
            while True:
                try:
                    with open("file.txt","w") as f:
                        f.write(app.config["SOURCE"]+" "+app.config["TARGET"])
                        app.config["TARGET"]=None
                        app.config["SOURCE"]=None
                        if(os.path.exists(os.path.join(basedir, "./static/a.jpg"))):
                            os.remove(os.path.join(basedir, "./static/a.jpg"))
                        if(os.path.exists(os.path.join(basedir, "./static/b.jpg"))):
                            os.remove(os.path.join(basedir, "./static/b.jpg"))
                        break
                except:
                    continue
    return render_template('index.html',image="../static/01.gif")

@app.route('/about',methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/works',methods=['GET', 'POST'])
def works():
    return render_template('works.html')

@app.route("/get-image",methods=["GET"])
def get_vote():
    image="../static/a.jpg"
    default="../static/01.gif"
    if(os.path.exists(os.path.join(basedir, "./static/a.jpg"))):
        return jsonify(image)
    return jsonify(default)

@app.route("/get-image2",methods=["GET"])
def get_vote2():
    image="../static/b.jpg"
    default="../static/01.gif"
    if(os.path.exists(os.path.join(basedir, "./static/b.jpg"))):
        return jsonify(image)
    return jsonify(default)
    
if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='x:x:x:x')