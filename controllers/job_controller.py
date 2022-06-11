import csv
import configparser
import os
import pathlib
import psycopg2
import re
import socket
import subprocess
import traceback
from datetime import datetime
from flask import render_template, redirect, url_for, request, session
from flask.helpers import make_response
from io import StringIO
from helpers.app_helper import AppHelper
from services.job_service import JobService

ERR_OTHER_TERM_UPDATE = '他端末で更新されています。画面内容を確認し、必要であれば再実行をお願いします。'
WAR_STATE_CHANGED = '他端末で実行状態が更新されています。'

class JobController:
    '''
    JobController - ジョブ
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


    def detail(self):
        '''
        ジョブ詳細
        '''
        message = None
        loops = None
        devices = None
        zabbix = None

        try:
            # request parameter
            tec_cd = session['tec_cd']
            job_id = request.form['jobId']
            job_status = request.form['status']

            # Service instanced
            service = JobService()
            job = service.get_job({'tec_cd': tec_cd, 'job_id':job_id})

            if job is None:
                return redirect(url_for('top'))

            if job_status and job['job_status_cd'] != job_status:
                message = WAR_STATE_CHANGED

            if job['job_status_cd'] == '020' or job['job_status_cd'] == '021': # 020:正常終了
                loops = service.get_loop_machine({'tec_cd': tec_cd, 'job_id':job_id})
                devices = service.get_unable_connect({'tec_cd': tec_cd, 'job_id':job_id})

                # 設定ファイルよりZabbix検索画面情報取得
                zabbix = self.setting.get('ZABBIX_URL')

            return render_template('job/job-detail.html', job=job, loops=loops, devices=devices, message=message, zabbix_url=zabbix)
        except Exception as e:
            print(traceback.format_exc())
            raise e


    def execute(self):
        '''
        ジョブ実行
        '''
        try:
            # parameter
            tec_cd = session['tec_cd']
            user_id = session['user']
            job_id = request.form['jobId']
            mod_time = request.form['modTime']
            sysdate = datetime.now()

            # ホスト名・IPアドレス取得
            # host = socket.gethostname()
            # ip_address = socket.gethostbyname(host)
            ip_address = request.remote_addr

            # Service instanced
            service = JobService()
            # database connect
            conn = psycopg2.connect(AppHelper.get_dsn())
            cur = conn.cursor()

            # 010:実行中の場合、強制終了指示
            job_status_cd = service.get_jos_status_cd({'tec_cd': tec_cd, 'job_id': job_id}, cur)
            if job_status_cd is not None and job_status_cd[0] == '010':

                # 実行状態更新
                job_param = {
                    'job_status_cd': '035', # 035:強制終了中
                    'ope_ip_address': ip_address,
                    'modified_timestamp': sysdate,
                    'modified_user_id': user_id,
                    'tec_cd': tec_cd,
                    'job_id': job_id,
                    'execution_cd': '010' # 010:実行中
                }
                service.update_job_termination(job_param, cur)

                # ログ登録
                log_param = {
                    'tec_cd': tec_cd,
                    'log_output_timestamp': sysdate,
                    'log_output_id': user_id,
                    'log_type_cd': '029', # 029:ジョブの強制終了指示
                    'job_id': job_id,
                    'error_content': None,
                    'ope_ip_address': ip_address,
                }
                service.insert_log(log_param, cur)

            # COMMIT
            conn.commit()

            return {'result': '0', 'route':url_for('top')}

        except Exception as e:
            print(traceback.format_exc())
            # ROLLBACK
            conn.rollback()
            raise e

        finally:
            if conn is not None:
                cur.close()
                conn.close()


    def download(self):
        '''
        CSV出力
        '''
        try:
            # parameter
            tec_cd = session['tec_cd']
            user_id = session['user']
            job_id = request.form['jobId']
            sysdate = datetime.now()
            strdate = datetime.strftime(sysdate, '%Y%m%d%H%M%S')

            # ホスト名・IPアドレス取得
            # host = socket.gethostname()
            # ip_address = socket.gethostbyname(host)
            ip_address = request.remote_addr

            # Service instanced
            service = JobService()
            loop = service.get_loop_machine({'tec_cd': tec_cd, 'job_id':job_id})

            # ログ登録
            log_param = {
                'tec_cd': tec_cd,
                'log_output_timestamp': sysdate,
                'log_output_id': user_id,
                'log_type_cd': '016', # 016:CSV出力
                'job_id': job_id,
                'error_content': None,
                'ope_ip_address': ip_address,
            }
            service.insert_log_csv(log_param)

            file = StringIO()
            writer = csv.writer(file, quoting=csv.QUOTE_NONE)

            # header
            writer.writerow(['ループ箇所フラグ', 'ホスト名', 'IPアドレス', 'ポート', 'タイプ', 'MACFLAP', '設置場所', 'VLAN'])
            # body
            for row in loop:
                writer.writerow([
                    "ループ箇所" if row['loop_flag'] == True else "ループ構成機器", 
                    row['hostname'],
                    row['ip_address'],
                    row['if_name'],
                    row['machine_type'],
                    row['macflap_count_per_min'],
                    row['location'],
                    row['vlan_id']
                ])

            res = make_response()
            res.data = file.getvalue().encode("utf_8_sig")
            res.headers['Content-Type'] = 'text/csv'
            res.headers['Content-Disposition'] = 'attachement; filename=LOOP_MACHINE_{}.csv'.format(strdate)
            return res

        except Exception as e:
            print(traceback.format_exc())
            raise e


    def create(self):
        '''
        ジョブ新規作成
        '''
        try:
            job_title = session["default_job_title"]
            bcast_time = session["default_bcast_time"]

            # 現在の日付取得
            sysdate = datetime.now()
            # YYYY/MM/DD ⇒ 日付変換
            job_title = re.sub(r'\w{4}/\w{2}/\w{2}', sysdate.strftime('%Y/%m/%d'), job_title)

            return render_template('job/job-create.html', job_title=job_title, bcast_time=bcast_time)
        except Exception as e:
            print(traceback.format_exc())
            raise e


    def regist(self):
        '''
        ジョブ登録
        '''
        try:
            # parameter
            MODE_SCREEN = '1'
            sysdate = datetime.now()
            tec_cd = session['tec_cd']
            job_id = '1001'
            user_id = session['user']
            title = request.form['title']
            create_user = request.form['creater']
            content = request.form['content']
            bcast_date = request.form['bcastDate']
            bcast_time = request.form['bcastTime']
            bcast_data_time = datetime.strptime('{} {}'.format(bcast_date,bcast_time), '%Y-%m-%d %H:%M')

            # ホスト名・IPアドレス取得
            # host = socket.gethostname()
            # ip_address = socket.gethostbyname(host)
            ip_address = request.remote_addr

            # Service instanced
            service = JobService()
            # database connect
            conn = psycopg2.connect(AppHelper.get_dsn())
            cur = conn.cursor()

            # ジョブID採番
            job = service.get_job_id({'tec_cd': tec_cd}, cur)
            if job is not None:
                job_id = job[0]

                # ジョブID管理更新
                param = {
                    'tec_cd': tec_cd,
                    'job_id': job_id,
                    'ope_ip_address': ip_address,
                    'modified_timestamp': sysdate,
                    'modified_user_id': user_id,
                }
                service.update_job_id(param, cur)

            else:
                # ジョブID管理登録
                param = {
                    'tec_cd': tec_cd,
                    'job_id': job_id,
                    'ope_ip_address': ip_address,
                    'created_timestamp': sysdate,
                    'created_user_id': user_id,
                    'modified_timestamp': sysdate,
                    'modified_user_id': user_id,
                }
                service.insert_job_id(param, cur)


            # ジョブ状態登録
            job_param = {
                'tec_cd': tec_cd,
                'job_id': job_id,
                'job_status_cd': '010', # 010:実行中
                'title': title,
                'create_user_name': create_user,
                'content': content,
                'use_bcast_timestamp': bcast_data_time,
                'start_timestamp': sysdate,
                'end_timestamp': None,
                'progress': 0,
                'ope_ip_address': ip_address,
                'del_flg': '0',
                'created_timestamp': sysdate,
                'created_user_id': user_id,
                'modified_timestamp': sysdate,
                'modified_user_id': user_id,
            }
            service.insert_job(job_param, cur)

            # ログ登録
            log_param = {
                'tec_cd': tec_cd,
                'log_output_timestamp': sysdate,
                'log_output_id': user_id,
                'log_type_cd': '020', # 020:ジョブの作成
                'job_id': job_id,
                'error_content': None,
                'ope_ip_address': ip_address,
            }
            service.insert_log(log_param, cur)

            # ジョブ実行
            subprocess.Popen(['python', self.setting.get('BATCH_FILE_PATH'), MODE_SCREEN, job_id])

            # COMMIT
            conn.commit()
            return {'result': '0', 'route':url_for('top')}

        except psycopg2.IntegrityError as Integrity:
            print(traceback.format_exc())
            # ROLLBACK
            conn.rollback()
            if Integrity.pgcode == '23505': #UniqueViolation
                return { 'result': '1', 'message':ERR_OTHER_TERM_UPDATE }
            else:
                raise Integrity

        except Exception as e:
            print(traceback.format_exc())
            # ROLLBACK
            conn.rollback()
            raise e

        finally:
            if conn is not None:
                cur.close()
                conn.close()


    def edit(self):
        '''
        ジョブ編集
        '''
        try:
            # parameter
            tec_cd = session['tec_cd']
            job_id = request.form['jobId']

            # Service instanced
            service = JobService()
            job = service.get_job_edit({'tec_cd': tec_cd, 'job_id':job_id})

            if job is None:
                return redirect(url_for('top'))

            return render_template('job/job-edit.html', job=job)
        except Exception as e:
            print(traceback.format_exc())
            raise e


    def update(self):
        '''
        ジョブ更新
        '''
        try:
            # parameter
            sysdate = datetime.now()
            tec_cd = session['tec_cd']
            user_id = session['user']
            job_id = request.form['jobId']
            title = request.form['title']
            create_user = request.form['creater']
            content = request.form['content']
            mod_time = request.form['modTime']

            # ホスト名・IPアドレス取得
            # host = socket.gethostname()
            # ip_address = socket.gethostbyname(host)
            ip_address = request.remote_addr

            # Service instanced
            service = JobService()
            # database connect
            conn = psycopg2.connect(AppHelper.get_dsn())
            cur = conn.cursor()

            # 他端末更新チェック
            latset = service.get_latset_date({'tec_cd': tec_cd, 'job_id': job_id}, cur)
            if latset is not None and latset[0] != mod_time:
                return { 'result': '1', 'message':ERR_OTHER_TERM_UPDATE }

            # ジョブ状態更新
            param = {
                'title': title,
                'create_user_name': create_user,
                'content': content,
                'ope_ip_address': ip_address,
                'modified_timestamp': sysdate,
                'modified_user_id': user_id,
                'tec_cd': tec_cd,
                'job_id': job_id
            }
            service.update_job_status(param, cur)

            # ログ登録
            log_param = {
                'tec_cd': tec_cd,
                'log_output_timestamp': sysdate,
                'log_output_id': user_id,
                'log_type_cd': '026', # 026:ジョブの編集
                'job_id': job_id,
                'error_content': None,
                'ope_ip_address': ip_address,
            }
            service.insert_log(log_param, cur)

            # commit transaction
            conn.commit()
            return {'result': '0', 'route':url_for('top')}

        except Exception as e:
            print(traceback.format_exc())
            # rollback transaction
            conn.rollback()
            raise e

        finally:
            if conn is not None:
                cur.close()
                conn.close()