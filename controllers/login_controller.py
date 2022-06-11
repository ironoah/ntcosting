import configparser
import os
import pathlib
import socket
import syslog
import traceback
from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, flash, request, session
from helpers.app_helper import AppHelper
from services.login_service import LoginService

ERR_USER_PASSWORD_INCORRECT = 'ユーザーIDまたはパスワードが間違っています。'
WAR_PASSWORD_EXPIRED = 'パスワードの有効期限が切れています。パスワードを変更して下さい。'

class LoginController:
    '''
    LoginController - ログイン
    '''
    def __init__(self):
        '''
        コンストラクタ
        '''
        try:
            path = os.path.join(pathlib.Path(os.path.dirname(__file__)).parent, 'config.ini')
            config = configparser.ConfigParser()
            config.read(path, 'utf_8_sig')
            self.setting = config['settings']
        except Exception as e:
            print(traceback.format_exc())
            raise e


    def index(self):
        '''
        ページロード
        '''
        try:
            # Service instanced
            service = LoginService()
            config = service.get_configuration({'tec_cd': self.setting.get('TEC_CD')})

            # セッション変数へ格納
            session['tec_cd'] = self.setting.get('TEC_CD')
            session['log_threshold'] = config['login_fail_count'] if config != None else 0

            return render_template('login.html')
        except Exception as e:
            print(traceback.format_exc())
            raise e


    def login(self):
        '''
        ログイン処理
        '''
        try:
            # request parameter
            tec_cd = session['tec_cd']
            user_id = request.form['userId']
            password = request.form['password']

            # ホスト名・IPアドレス取得
            # host = socket.gethostname()
            # ip_address = socket.gethostbyname(host)
            ip_address = request.remote_addr

            # Service instanced
            service = LoginService()
            account = service.get_account({
                                    'tec_cd': tec_cd,
                                    'account_id': user_id,
                                    'password': AppHelper.calculate_hash(password, self.setting.get('PASSWORD_SALT'))
                                })

            # ユーザー認証
            if account is not None:
                # 認証成功

                # セッション変数へ格納
                session.permanent = True
                session["user"] = account['account_id']
                session["job_lines_page"] = account['job_lines_page']
                session["default_bcast_time"] = account['default_bcast_time']
                session["default_job_title"] = account['default_job_title']
                session["log_lines_page"] = account['log_lines_page']

                # パスワード有効期限チェック
                if account['password_mod_timestamp'] is not None and account['password_mod_term'] is not None:
                    expired_date = account['password_mod_timestamp'] + timedelta(days = account['password_mod_term'])
                    current_date = datetime.now()

                    if (current_date > expired_date):
                        flash(WAR_PASSWORD_EXPIRED)
                
                param = {
                    'tec_cd': tec_cd,
                    'log_output_timestamp': datetime.now(),
                    'log_output_id': user_id,
                    'log_type_cd': '010', # 010:ログイン成功
                    'error_content': None,
                    'ope_ip_address': ip_address,
                }
                # ログテーブル登録
                service.insert_log(param)

                return redirect(url_for('top'))
            else:
                # 認証失敗

                param = {
                    'tec_cd': tec_cd,
                    'log_output_timestamp': datetime.now(),
                    'log_output_id': user_id,
                    'log_type_cd': '011', # 011:ログイン失敗
                    'error_content': 'ログインに失敗しました',
                    'ope_ip_address': ip_address,
                }
                # ログテーブル登録
                service.insert_log(param)

                # ブルートフォースアタック検知
                threshold = service.get_logincount({'tec_cd': tec_cd, 'log_type_cd': '011'})
                if threshold is not None and session['log_threshold'] < threshold['login_count']:
                    
                    param = {
                        'tec_cd': tec_cd,
                        'log_output_timestamp': datetime.now(),
                        'log_output_id': user_id,
                        'log_type_cd': '012', # 012:ブルートフォースアタック検知
                        'error_content': 'ブルートフォースアタックを検知しました',
                        'ope_ip_address': ip_address,
                    }
                    # ログテーブル登録
                    service.insert_log(param)

                    # syslog出力
                    syslog.syslog(syslog.LOG_WARNING, 'Detected brute force attack!')

                return render_template('login.html', message = ERR_USER_PASSWORD_INCORRECT)
        except Exception as e:
            print(traceback.format_exc())
            raise e


    def logout(self):
        '''
        ログアウト処理
        '''
        try:
            # ホスト名・IPアドレス取得
            # host = socket.gethostname()
            # ip_address = socket.gethostbyname(host)
            ip_address = request.remote_addr

            # Service instanced
            service = LoginService()
            param = {
                'tec_cd': session['tec_cd'],
                'log_output_timestamp': datetime.now(),
                'log_output_id': session["user"],
                'log_type_cd': '013', # 013:ログアウト
                'error_content': None,
                'ope_ip_address': ip_address,
            }
            # ログテーブル登録
            service.insert_log(param)

            session.pop('user', None)
            return redirect(url_for('index'))
        except Exception as e:
            print(traceback.format_exc())
            raise e