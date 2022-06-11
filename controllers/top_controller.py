import json
import psycopg2
import socket
import traceback
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import render_template, url_for, request, session
from helpers.app_helper import AppHelper
from services.top_service import TopService

ERR_NOT_CREATE_JOB = '実行中のジョブが2件以上存在する為、ジョブを新規登録できません。'
ERR_OTHER_TERM_UPDATE = '他端末で更新されています。画面内容を確認し、必要であれば再実行をお願いします。'

class TopController:
    '''
    TopController - Top
    '''
    def __init__(self):
        '''
        コンストラクタ
        '''


    def index(self):
        '''
        ページロード
        '''
        try:
            # セッション削除
            session.pop('search_conditions', None)
            # セッション取得
            tec_cd = session['tec_cd']
            page_length = session['job_lines_page']

            # 現在の日付取得
            today = datetime.today()
            one_month_ago = today - relativedelta(months=1)
            # 日付 ⇒ 文字列
            from_date = datetime.strftime(one_month_ago, '%Y-%m-%d')
            to_date = datetime.strftime(today, '%Y-%m-%d')

            # Service instanced
            service = TopService()
            jobs = service.get_job({'tec_cd': tec_cd, 'from_date': from_date, 'to_date': to_date})

            return render_template('top/top.html', jobs=jobs, job_page_length=page_length, from_date=from_date, to_date=to_date)
        except Exception as e:
            print(traceback.format_exc())
            raise e


    def back(self):
        '''
        ページロード(検索条件維持)
        '''
        try:
            # セッション取得
            tec_cd = session['tec_cd']
            page_length = session['job_lines_page']

            # 検索条件が保持されているか判定
            if "search_conditions" not in session:
                # 現在の日付取得
                today = datetime.today()
                one_month_ago = today - relativedelta(months=1)
                # 日付 ⇒ 文字列
                from_date = datetime.strftime(one_month_ago, '%Y-%m-%d')
                to_date = datetime.strftime(today, '%Y-%m-%d')
            else:
                conditions = session['search_conditions']
                from_date = conditions['from_date']
                to_date = conditions['to_date']

            # Service instanced
            service = TopService()
            jobs = service.get_job({'tec_cd': tec_cd, 'from_date': from_date, 'to_date': to_date})

            return render_template('top/top.html', jobs=jobs, job_page_length=page_length, from_date=from_date, to_date=to_date)

        except Exception as e:
            print(traceback.format_exc())
            raise e


    def search(self):
        '''
        検索処理
        '''
        try:
            # parameter
            param = {
                'tec_cd': session['tec_cd'],
                'from_date': request.form['fromDate'],
                'to_date': request.form['toDate'],
            }

            # Service instanced
            service = TopService()
            jobs = service.get_job(param)

            # 検索条件保持
            session['search_conditions'] = param

            return {'result': '0', 'template': render_template('top/top-table.html', jobs=jobs)}
        except Exception as e:
            print(traceback.format_exc())
            raise e


    def checkstatus(self):
        '''
        ジョブ実行状態判定
        '''
        try:
            # Service instanced
            service = TopService()

            # 実行中のジョブ件数取得
            job = service.get_jobcount({'tec_cd': session['tec_cd']})
            job_count = job['job_count'] if job != None else 0

            return {'count': job_count, 'message':ERR_NOT_CREATE_JOB}
        except Exception as e:
            print(traceback.format_exc())
            raise e


    def execute(self):
        '''
        ジョブ実行
        '''
        try:
            # parameter
            process = request.form['process']
            jobs = request.form['jobs']
            tec_cd = session['tec_cd']
            user_id = session['user']
            sysdate = datetime.now()

            # JSON ⇒ Dictionary
            json_dict = json.loads(jobs)

            # ホスト名・IPアドレス取得
            # host = socket.gethostname()
            # ip_address = socket.gethostbyname(host)
            ip_address = request.remote_addr

            # Service instanced
            service = TopService()
            # database connect
            conn = psycopg2.connect(AppHelper.get_dsn()) 
            cur = conn.cursor()

            # 強制終了
            if process == '1':
                # 選択されたジョブ件数分、ループ
                for job in json_dict:
                    job_id = job['job_id']
                    mod_time = job['mod_time']

                    # 010:実行中の場合、強制終了指示
                    job_status_cd = service.get_jos_status_cd({'tec_cd': tec_cd, 'job_id': job_id}, cur)
                    if job_status_cd is not None and job_status_cd[0] == '010':

                        # 実行状態更新(強制終了)
                        status_param = {
                            'job_status_cd': '035', # 035:強制終了中
                            'ope_ip_address': ip_address,
                            'modified_timestamp': sysdate,
                            'modified_user_id': user_id,
                            'tec_cd': tec_cd,
                            'job_id': job_id,
                            'execution_cd': '010', # 010:実行中
                        }
                        service.update_job_termination(status_param, cur)

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

            # 削除
            else:
                # 選択されたジョブ件数分、ループ
                for job in json_dict:
                    job_id = job['job_id']
                    mod_time = job['mod_time']

                    # 他端末更新チェック
                    latset = service.get_latset_date({'tec_cd': tec_cd, 'job_id': job_id}, cur)
                    if latset is not None and latset[0] != mod_time:
                        return { 'result': '1', 'message':ERR_OTHER_TERM_UPDATE }

                    # 実行状態更新(削除)
                    status_param = {
                        'ope_ip_address': ip_address,
                        'modified_timestamp': sysdate,
                        'modified_user_id': user_id,
                        'tec_cd': tec_cd,
                        'job_id': job_id,
                    }
                    service.update_job_delete(status_param, cur)

                    # ログ登録
                    log_param = {
                        'tec_cd': tec_cd,
                        'log_output_timestamp': sysdate,
                        'log_output_id': user_id,
                        'log_type_cd': '028', # 028:削除
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