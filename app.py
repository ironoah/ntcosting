#-*- coding:utf-8 -*-
import configparser
import os
import subprocess
from datetime import timedelta
from flask import Flask, render_template, redirect, url_for, session, request
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound
from controllers.job_controller import JobController
from controllers.log_controller import LogController
from controllers.login_controller import LoginController
from controllers.setting_controller import SettingController
from controllers.top_controller import TopController
from helpers.app_helper import AppHelper

# ----------------------------------------
# 定数(メッセージ)
# ----------------------------------------
ERR_SESSION_TIMEOUT = '未認証またはセッションがタイムアウトしました。お手数ですが、ログインしていただけますようお願いいたします。'
ERR_ILLEGAL_ACCESS = '不正なURLのアクセスが検出されました。'
ERR_SYSTEM_EXCEPTION = 'アプリケーションで障害が発生しました。システム管理者にご連絡ください。'

# ----------------------------------------
# iniファイル読込
# ----------------------------------------
path = os.path.join(os.path.dirname(__file__), 'config.ini')
config = configparser.ConfigParser()
config.read(path, 'utf_8_sig')
settings = config['settings']
lifetime = settings.getint('SESSION_LIFE_TIME', 10)

# ----------------------------------------
# Flask
# ----------------------------------------
app = Flask(__name__)
app.secret_key = "tani_secret"
app.permanent_session_lifetime = timedelta(minutes=lifetime) 


# Index
@app.route('/')
def index():
    try:
        ctrl = LoginController()
        return ctrl.index()
    except Exception as e:
        return e


# Login
@app.route('/login', methods=['POST'])
def login():
    try:
        ctrl = LoginController()
        return ctrl.login()
    except Exception as e:
        return e


# Logout
@app.route('/logout')
def logout():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return redirect(url_for('index'))

        ctrl = LoginController()
        return ctrl.logout()
    except Exception as e:
        return e


# TOP
@app.route('/top')
def top():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return render_template('error.html', err_content = ERR_SESSION_TIMEOUT)

        ctrl = TopController()
        return ctrl.index()
    except Exception as e:
        return e


# TOP (検索条件維持)
@app.route('/top/back')
def top_back():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return render_template('error.html', err_content = ERR_SESSION_TIMEOUT)

        ctrl = TopController()
        return ctrl.back()
    except Exception as e:
        return e


# TOP (検索)
@app.route('/top/search', methods=['POST'])
def top_search():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return {'result':'9', 'route':url_for('error')}
        
        ctrl = TopController()
        return ctrl.search()
    except Exception as e:
        return e


# TOP (ジョブ新規作成)
@app.route('/top/check-status')
def checkstatus():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return render_template('error.html', err_content = ERR_SESSION_TIMEOUT)

        ctrl = TopController()
        return ctrl.checkstatus()
    except Exception as e:
        return e


# TOP (ジョブ実行)
@app.route('/top/execute', methods=['POST'])
def execute():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return {'result': '9', 'route':url_for('error')}

        ctrl = TopController()
        return ctrl.execute()
    except Exception as e:
        return e


# ジョブ新規作成
@app.route('/top/job-create')
def jobcreate():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return render_template('error.html', err_content = ERR_SESSION_TIMEOUT)

        ctrl = JobController()
        return ctrl.create()
    except Exception as e:
        return e


# ジョブ新規作成(登録)
@app.route('/top/job-create/regist', methods=['POST'])
def jobregist():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return {'result':'9', 'route':url_for('error')}

        ctrl = JobController()
        return ctrl.regist()
    except Exception as e:
        return e


# ジョブ詳細
@app.route('/top/job-detail', methods=['POST'])
def jobdetail():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return render_template('error.html', err_content = ERR_SESSION_TIMEOUT)

        ctrl = JobController()
        return ctrl.detail()
    except Exception as e:
        return e


# ジョブ詳細 (強制終了)
@app.route('/top/job-detail/execute', methods=['POST'])
def jobdetail_execute():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return {'result':'9', 'route':url_for('error')}

        ctrl = JobController()
        return ctrl.execute()
    except Exception as e:
        return e


# ジョブ詳細 (CSV出力)
@app.route('/top/job-detail/download', methods=['POST'])
def jobdetail_download():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return render_template('error.html', err_content = ERR_SESSION_TIMEOUT)

        ctrl = JobController()
        return ctrl.download()
    except Exception as e:
        return e


# ジョブ編集
@app.route('/top/job-edit', methods=['POST'])
def jobedit():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return render_template('error.html', err_content = ERR_SESSION_TIMEOUT)

        ctrl = JobController()
        return ctrl.edit()
    except Exception as e:
        return e


# ジョブ編集 (更新)
@app.route('/top/job-edit/update', methods=['POST'])
def jobupdate():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return {'result':'9', 'route':url_for('error')}

        ctrl = JobController()
        return ctrl.update()
    except Exception as e:
        return e


# ログ
@app.route('/top/log')
def log():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return render_template('error.html', err_content = ERR_SESSION_TIMEOUT)
        
        ctrl = LogController()
        return ctrl.index()
    except Exception as e:
        return e


# ログ (検索)
@app.route('/top/log/search', methods=['POST'])
def log_search():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return {'result':'9', 'route':url_for('error')}
        
        ctrl = LogController()
        return ctrl.search()
    except Exception as e:
        return e


# ログ (CSV出力)
@app.route('/top/log/csv-download', methods=['POST'])
def log_csv_download():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return render_template('error.html', err_content = ERR_SESSION_TIMEOUT)
        
        ctrl = LogController()
        return ctrl.csv_download()
    except Exception as e:
        return e


# ログ (Txt出力)
@app.route('/top/log/txt-download', methods=['POST'])
def log_txt_download():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return render_template('error.html', err_content = ERR_SESSION_TIMEOUT)
        
        ctrl = LogController()
        return ctrl.txt_download()
    except Exception as e:
        return e


# 設定 (一般設定)
@app.route('/top/setting/general')
def setting_general():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return render_template('error.html', err_content = ERR_SESSION_TIMEOUT)

        ctrl = SettingController()
        return ctrl.general()
    except Exception as e:
        return e


# 設定 (一般設定更新)
@app.route('/top/setting/general/update', methods=['POST'])
def setting_update():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return {'result':'9', 'route':url_for('error')}
        
        ctrl = SettingController()
        return ctrl.general_update()
    except Exception as e:
        return e


# 設定 (デフォルト)
@app.route('/top/setting/general/default')
def setting_default():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return {'result':'9', 'route':url_for('error')}
        
        ctrl = SettingController()
        return ctrl.default()
    except Exception as e:
        return e


# 設定 (CSV出力)
@app.route('/top/setting/general/download', methods=['POST'])
def setting_download():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return render_template('error.html', err_content = ERR_SESSION_TIMEOUT)
        
        ctrl = SettingController()
        return ctrl.download()
    except Exception as e:
        return e


# 設定 (アカウント)
@app.route('/top/setting/account')
def setting_account():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return render_template('error.html', err_content = ERR_SESSION_TIMEOUT)

        ctrl = SettingController()
        return ctrl.account()
    except Exception as e:
        return e


# 設定 (アカウント更新)
@app.route('/top/setting/account/update', methods=['POST'])
def account_update():
    try:
        if "user" not in session:
            AppHelper.session_timeout()
            return {'result':'9', 'route':url_for('error')}

        ctrl = SettingController()
        return ctrl.account_update()
    except Exception as e:
        return e


# 画面終了
@app.route('/close')
def close():
    AppHelper.window_close()
    return ('',204)


# エラー
@app.route('/error')
def error():
    try:
        if "user" not in session:
            # session timeout
            return render_template('error.html', err_content = ERR_SESSION_TIMEOUT)
        else:
            # system error
            return render_template('error.html', err_content = ERR_SYSTEM_EXCEPTION)

    except Exception as e:
        raise e


# Web API
@app.route('/api/looptool', methods=['GET'])
def api_execute():
    try:
        # 実行バッチパス取得
        batch_path = settings.get('BATCH_FILE_PATH')
        # Zabbixサーバー IPアドレス取得
        zabbix_ip = settings.get('ZABBIX_HOST')
        # アクセス元IPアドレス取得
        remote_ip = request.remote_addr

        # ZabbixからのIPのみ許可
        if zabbix_ip == remote_ip:

            # 自動実行のジョブ件数が0件の場合、実行
            if AppHelper.running_auto_job_count() == 0:
                # バッチ処理実行
                subprocess.Popen(['python', batch_path, '2'])

        return ('',200)
    
    except Exception as e:
        print(repr(e))
        return ('',204)


# BadRequest/NotFound
@app.errorhandler(NotFound)
@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return render_template('error.html', err_content = ERR_ILLEGAL_ACCESS)


# InternalServerError
@app.errorhandler(InternalServerError)
@app.errorhandler(Exception)
def handle_exception(e):
    return render_template('error.html', err_content = ERR_SYSTEM_EXCEPTION)


if __name__ == '__main__':
    app.run(debug=False)