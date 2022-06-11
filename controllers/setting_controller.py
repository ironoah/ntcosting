import configparser
import csv
import os
import pathlib
import psycopg2
import psycopg2.extras
import socket
import traceback
from datetime import datetime
from flask import render_template, url_for, request, session
from flask.helpers import make_response
from io import StringIO
from helpers.app_helper import AppHelper
from services.setting_service import SettingService

ERR_OTHER_TERM_UPDATE = '他端末で更新されています。画面内容を確認し、必要であれば再実行をお願いします。'

class SettingController:
    '''
    SettingController - 設定
    '''
    def __init__(self):
        '''
        コンストラクタ
        '''
        try:
            path = os.path.join(pathlib.Path(os.path.dirname(__file__)).parent, 'config.ini')
            config = configparser.ConfigParser()
            config.read(path, 'utf_8_sig')
            self.settings = config['settings']
        except Exception as e:
            print(traceback.format_exc())
            raise e


    def general(self):
        '''
        初期表示(一般設定)
        '''
        try:
            # TEC_CD
            tec_cd = session['tec_cd']

            # Service instanced
            service = SettingService()
            log_lvl = service.get_log_lvl({'tec_cd': tec_cd})
            setting = service.get_setting({'tec_cd': tec_cd})

            if setting is None:
                # 設定情報がない場合、設定ファイルより取得
                setting = self.default_setting()

            return render_template('setting/setting-general.html', log_lvl=log_lvl, setting=setting)
        except Exception as e:
            print(traceback.format_exc())
            raise e


    def general_update(self):
        '''
        更新処理(一般設定)
        '''
        try:
            # session param
            tec_cd = session['tec_cd']
            user_id = session['user']
            mod_time = request.form['modTime']

            # ホスト名・IPアドレス取得
            # host = socket.gethostname()
            # ip_address = socket.gethostbyname(host)
            ip_address = request.remote_addr

            # Service instanced
            service = SettingService()
            # database connenct
            conn = psycopg2.connect(AppHelper.get_dsn())
            conn.cursor_factory = psycopg2.extras.DictCursor
            cur = conn.cursor()

            # 他端末更新チェック
            latset = service.get_latset_date({'tec_cd': tec_cd}, cur)
            if latset is not None and latset[0] != mod_time:
                return { 'result': '1', 'message': ERR_OTHER_TERM_UPDATE }

            # 現在の設定情報取得
            curr_setting = service.get_current_setting({'tec_cd': tec_cd}, cur)
            if curr_setting is not None:

                # 定期実行間隔が変更された場合、データ初期化
                if curr_setting['regular_execute_cycle'] != int(request.form['regularExecuteCycle']):
                    service.delete_regular_execute({'tec_cd':tec_cd, 'created_timestamp':datetime.now().replace(microsecond=0)}, cur)

            # 一般設定情報更新
            param = {
                'job_lines_page': request.form['jobLinesPage'],
                'data_get_timeout': request.form['dataGetTimeout'],
                'default_bcast_time': request.form['defaultBcastTime'],
                'macflap_get_time': request.form['macflapGetTime'],
                'broadcast_get_time': request.form['broadcastGetTime'],
                'default_job_title': request.form['defaultJobTitle'],
                'auto_job_title': request.form['autoJobTitle'],
                'output_log_lvl_cd': request.form['outputLogLvl'],
                'stock_term': request.form['stockTerm'],
                'log_lines_page': request.form['logLinesPage'],
                'login_fail_count': request.form['loginFailCount'],
                'password_mod_term': request.form['passwordModTerm'],
                'regular_job_title': request.form['regularJobTitle'],
                'regular_execute_cycle': request.form['regularExecuteCycle'],
                'regular_execute_time': request.form['regularExecuteTime'],
                'from_mail_address': request.form['fromMailAddress'],
                'to_mail_address': request.form['toMailAddress'],
                'ope_ip_address': ip_address,
                'modified_timestamp': datetime.now(),
                'modified_user_id': user_id,
                'tec_cd': tec_cd
            }
            service.update_general(param, cur)

            # 最新設定情報取得
            setting = service.get_latset_setting({'tec_cd': tec_cd}, cur)
            if setting is not None:
                # セッション変数へ格納
                session["job_lines_page"] = setting['job_lines_page']
                session["default_bcast_time"] = setting['default_bcast_time']
                session["default_job_title"] = setting['default_job_title']
                session["log_lines_page"] = setting['log_lines_page']

            # COMMIT
            conn.commit()
            return { 'result': '0', 'route':url_for('top') }

        except Exception as e:
            print(traceback.format_exc())
            # ROLLBACK
            conn.rollback()
            raise e

        finally:
            if conn is not None:
                cur.close()
                conn.close()


    def default(self):
        '''
        デフォルト(一般設定)
        '''
        try:
            setting = self.default_setting()
            return {'result':'0', 'setting':setting}
        except Exception as e:
            print(traceback.format_exc())
            raise e


    def download(self):
        '''
        設定情報CSV出力
        '''
        try:
            # parameter
            tec_cd = session['tec_cd']
            user_id = session['user']
            sysdate = datetime.now()
            strdate = datetime.strftime(sysdate, '%Y%m%d%H%M%S')

            # ホスト名・IPアドレス取得
            # host = socket.gethostname()
            # ip_address = socket.gethostbyname(host)
            ip_address = request.remote_addr

            # Service instanced
            service = SettingService()
            config = service.get_setting({'tec_cd': tec_cd})

            # ログ登録
            log_param = {
                'tec_cd': tec_cd,
                'log_output_timestamp': sysdate,
                'log_output_id': user_id,
                'log_type_cd': '016', # 016:CSV出力
                'job_id': None,
                'error_content': None,
                'ope_ip_address': ip_address,
            }
            service.insert_log(log_param)

            file = StringIO()
            writer = csv.writer(file, quoting=csv.QUOTE_NONE)

            # header
            writer.writerow(['1ページ表示数(TOP画面)', '情報取得タイムアウト(秒)', 'MACFLAP数取得基準時間(分)', 'ブロードキャスト数取得基準時間(分)', '使用BCAST時間初期値', 'ジョブタイトル初期値', 'ジョブタイトル(自動実行)', '出力ログレベル', '保存期間(日)',
                             '1ページ表示数(ログ画面)', 'ブルートフォースアタック検知ログ閾値', 'ジョブタイトル(定期実行)', '定期実行間隔(日)', '定期実行時間', 'パスワード変更期間(日)', '送信元メールアドレス', '送信先メールアドレス'])
            # body
            if config is not None:
                writer.writerow([
                    config['job_lines_page'],
                    config['data_get_timeout'],
                    config['macflap_get_time'],
                    config['default_bcast_time'],
                    config['broadcast_get_time'],
                    config['default_job_title'],
                    config['auto_job_title'],
                    config['log_lvl_name'],
                    config['stock_term'],
                    config['log_lines_page'],
                    config['login_fail_count'],
                    config['regular_job_title'],
                    config['regular_execute_cycle'],
                    config['regular_execute_time'],
                    config['password_mod_term'],
                    config['from_mail_address'],
                    config['to_mail_address'],
                ])

            res = make_response()
            res.data = file.getvalue().encode("utf_8_sig")
            res.headers['Content-Type'] = 'text/csv'
            res.headers['Content-Disposition'] = 'attachement; filename=CONFIGURATION_{}.csv'.format(strdate)
            return res

        except Exception as e:
            print(traceback.format_exc())
            raise e


    def account(self):
        '''
        初期表示(アカウント)
        '''
        try:
            # TEC_CD
            tec_cd = session['tec_cd']

            # Service instanced
            service = SettingService()
            setting = service.get_setting({'tec_cd': tec_cd})

            return render_template('setting/setting-account.html', setting=setting)
        except Exception as e:
            print(traceback.format_exc())
            raise e


    def account_update(self):
        '''
        更新処理(アカウント)
        '''
        try:
            # TEC_CD
            tec_cd = session['tec_cd']
            user_id = session['user']
            mod_time = request.form['modTime']
            account_id = request.form['user']
            password = AppHelper.calculate_hash(request.form['password'], self.settings.get('PASSWORD_SALT'))

            # ホスト名・IPアドレス取得
            # host = socket.gethostname()
            # ip_address = socket.gethostbyname(host)
            ip_address = request.remote_addr

            # Service instanced
            service = SettingService()
            # database connect
            conn = psycopg2.connect(AppHelper.get_dsn())
            conn.cursor_factory = psycopg2.extras.DictCursor
            cur = conn.cursor()
                    
            # 他端末更新チェック
            latset = service.get_latset_date({'tec_cd': tec_cd}, cur)
            if latset is not None and latset[0] != mod_time:
                return { 'result': '1', 'message': ERR_OTHER_TERM_UPDATE }

            # アカウント情報更新
            param = {
                'account_id': account_id,
                'password': password,
                'password_mod_timestamp': datetime.now(),
                'ope_ip_address': ip_address,
                'modified_timestamp': datetime.now(),
                'modified_user_id': user_id,
                'tec_cd': tec_cd
            }
            service.update_account(param, cur)

            # 最新設定情報取得
            setting = service.get_latset_setting({'tec_cd': tec_cd}, cur)
            if setting is not None:
                # セッション変数へ格納
                session["user"] = setting['account_id']

            # COMMIT
            conn.commit()
            return { 'result': '0', 'route':url_for('top') }

        except Exception as e:
            print(traceback.format_exc())
            # ROLLBACK
            conn.rollback()
            raise e

        finally:
            if conn is not None:
                cur.close()
                conn.close()


    def default_setting(self):
        '''
        デフォルト値設定
        '''
        # 設定ファイル情報取得
        setting = {
            'job_lines_page': self.settings.get('JOB_LINES_PAGE'),
            'data_get_timeout': self.settings.get('DATA_GET_TIMEOUT'),
            'macflap_get_time': self.settings.get('MACFLAP_GET_TIME'),
            'broadcast_get_time': self.settings.get('BROADCAST_GET_TIME'),
            'default_bcast_time': self.settings.get('DEFAULT_BCAST_TIME'),
            'default_job_title': self.settings.get('DEFAULT_JOB_TITLE'),
            'auto_job_title': self.settings.get('AUTO_JOB_TITLE'),
            'output_log_lvl_cd': self.settings.get('OUTPUT_LOG_LVL'),
            'stock_term': self.settings.get('STOCK_TERM'),
            'log_lines_page': self.settings.get('LOG_LINES_PAGE'),
            'login_fail_count': self.settings.get('LOGIN_FAIL_COUNT'),
            'regular_job_title': self.settings.get('REGULAR_JOB_TITLE'),
            'regular_execute_cycle': self.settings.get('REGULAR_EXECUTE_CYCLE'),
            'regular_execute_time': self.settings.get('REGULAR_EXECUTE_TIME'),
            'password_mod_term': self.settings.get('PASSWORD_MOD_TERM'),
        }

        return setting