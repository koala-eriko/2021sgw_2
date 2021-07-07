# -----------------------------------------------
# 必要なモジュールをインポート
# -----------------------------------------------
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
import os
import os.path
import time
import datetime

# -----------------------------------------------
# configを設定
# -----------------------------------------------
# DB接続用のデータを設定
from werkzeug.utils import secure_filename

#ここは任意で設定する
USERNAME = "koala"
PASSWORD = "koala"

# -----------------------------------------------
# メソッドを定義
# -----------------------------------------------
# インスタンスの生成
app = Flask(__name__)
app.secret_key = 'hogehoge'

# アップロード先のフォルダを指定
UPLOAD_FOLDER1 = './static/image/'
app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1
UPLOAD_FOLDER2 = './static/des/'
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2

# configの読み込み
app.config.from_object(__name__)


# URL = http://127.0.0.1:5000/
@app.route('/')
def main_page():
    title = "main_page"
    name = app.config['USERNAME']
    return render_template("index.html", title=title, name=name)


# URL = http://127.0.0.1:5000/login
@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('main_page'))
    return render_template('login.html', error=error)


# URL = http://127.0.0.1:5000/logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('main_page'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # 画像とテキストを読み込む
        img_file = request.files['img_file']
        description = request.form.get('description')

        # ファイル名を取得する
        filename = secure_filename(img_file.filename)
        #filenameを変更するとややこしいことになったのでxに入れる
        x = str(filename)

        #imageのリストを取得してその長さをaに格納する
        files = os.listdir('./static/image/')
        a = int(len(files)) 
        #画像の名前を変更する（これで投稿した順番になる！！）
        x = str(a) + ".jpg"

        #テキストファイル名をつくる
        y = str(a) + ".txt"


        # アップロード先URLを生成する
        img_url = os.path.join(app.config['UPLOAD_FOLDER1'], str(a)+".jpg")
        des_url = os.path.join(app.config['UPLOAD_FOLDER2'], str(a)+".txt")
        #テキストファイルに書き込み
        f = open(des_url, "w")
        f.write(description) 
        f.close()
  
        # アップロード先に保存する
        img_file.save(img_url)



        # 画像をWEBページに表示する（表示されないけどとりあえず何か返すようにしておく。。）
        return render_template('index.html')

    else:
        # 書庫ページを表示する
        return redirect(url_for('index'))

# URL = http://127.0.0.1:5000/showall
@app.route('/showall')
def showall():
    return render_template('showall.html')

# 主処理
if __name__ == "__main__":
    # 起動
    app.run(debug=True)
