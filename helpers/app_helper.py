import configparser
import hashlib
import os
import pathlib
import socket
import traceback
from datetime import datetime
from flask import session, request
from services.login_service import LoginService
from services.job_service import JobService

class AppHelper:
    '''
    App共通ヘルパークラス
    '''

    @staticmethod
    def get_dsn():
        '''
        DB接続文字列
        ----------
        Return
            str : DB接続文字列
        '''
        path = os.path.join(pathlib.Path(os.path.dirname(__file__)).parent, 'config.ini')
        config = configparser.ConfigParser()
        config.read(path, 'utf_8_sig')
        db_config = config['db_connection']
        dsn = ("host='{0}' port={1} dbname={2} user={3} password='{4}'"
                .format(db_config['DB_HOST'], db_config['DB_PORT'], db_config['DB_NAME'], db_config['DB_USER'], db_config['DB_PASS']))

        return dsn


    @staticmethod
    def calculate_hash(password, salt):
        '''
        ハッシュ計算
        Parameters
        ----------
        password : str
            パスワード
        salt : str
            ソルト
        Returns
        ----------
        res:
            ハッシュ化された値
        '''
        # パスワード + saltをハッシュ化
        res = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        return res


    @staticmethod
    def window_close():
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
                'log_type_cd': '014', # 014:ログアウト(画面終了)
                'error_content': None,
                'ope_ip_address': ip_address,
            }
            # ログテーブル登録
            service.insert_log(param)

            # セッション削除
            session.pop('user', None)
            return

        except Exception as e:
            print(traceback.format_exc())
            raise e


    @staticmethod
    def session_timeout():
        '''
        セッションタイムアウト処理
        '''
        try:
            # TECコード取得
            path = os.path.join(pathlib.Path(os.path.dirname(__file__)).parent, 'config.ini')
            config = configparser.ConfigParser()
            config.read(path, 'utf_8_sig')
            setting = config['settings']

            # ホスト名・IPアドレス取得
            # host = socket.gethostname()
            # ip_address = socket.gethostbyname(host)
            ip_address = request.remote_addr

            param = {
                'tec_cd': setting.get('TEC_CD'),
                'log_output_timestamp': datetime.now(),
                'log_output_id': 'system',
                'log_type_cd': '015', # 015:セッションタイムアウト
                'error_content': None,
                'ope_ip_address': ip_address,
            }

            # Service instanced
            service = LoginService()
            service.insert_log(param)

            return

        except Exception as e:
            print(traceback.format_exc())
            raise e


    @staticmethod
    def running_auto_job_count() -> int:
        '''
        自動実行件数取得処理
        '''
        try:
            # TECコード取得
            path = os.path.join(pathlib.Path(os.path.dirname(__file__)).parent, 'config.ini')
            config = configparser.ConfigParser()
            config.read(path, 'utf_8_sig')
            setting = config['settings']

            param = {
                'tec_cd': setting.get('TEC_CD'),
                'job_status_cd': '010',
                'create_user_name': '自動実行',
                'del_flg': '0'
            }

            # Service instanced
            service = JobService()
            count = service.get_auto_count(param)

            return count

        except Exception as e:
            print(traceback.format_exc())
            raise e