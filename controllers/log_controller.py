import csv
import socket
import traceback
from datetime import datetime
from flask import render_template, request, session
from flask.helpers import make_response
from io import StringIO
from services.log_service import LogService

ERR_OTHER_TERM_UPDATE = '他端末で更新されています。画面内容を確認し、必要であれば再実行をお願いします。'

class LogController:
    '''
    LogController - ログ
    '''
    def __init__(self):
        '''
        コンストラクタ
        '''


    def index(self):
        '''
        初期表示
        '''
        try:
            # セッション取得
            tec_cd = session['tec_cd']
            page_length = session['log_lines_page']

            # Service instanced
            service = LogService()
            log_lvl = service.get_log_lvl({'tec_cd': tec_cd})
            logs = service.get_log({'tec_cd': tec_cd})

            return render_template('log/log.html', log_lvl=log_lvl, logs=logs, log_page_length=page_length)
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
                'log_lvl_cd': request.form['selectLogLvl'],
                'title': '%{}%'.format(request.form['jobTitle']) if request.form['jobTitle'] != '' else None,
                'from_date': request.form['fromDate'],
                'to_date': request.form['toDate'],
            }

            # Service instanced
            service = LogService()
            logs = service.search_log(param)

            return {'result': '0', 'template': render_template('log/log-table.html', logs=logs)}
        except Exception as e:
            print(traceback.format_exc())
            raise e


    def csv_download(self):
        '''
        CSV出力
        '''
        try:
            # parameter
            tec_cd = session['tec_cd']
            user_id = session['user']
            log_lvl_cd = request.form['selectLogLvl']
            title = '%{}%'.format(request.form['jobTitle']) if request.form['jobTitle'] != '' else None
            from_date = request.form['fromDate']
            to_date = request.form['toDate']
            sysdate = datetime.now()
            strdate = datetime.strftime(sysdate, '%Y%m%d%H%M%S')

            # ホスト名・IPアドレス取得
            # host = socket.gethostname()
            # ip_address = socket.gethostbyname(host)
            ip_address = request.remote_addr

            # Service instanced
            service = LogService()
            # ログ情報取得
            param = {
                'tec_cd': tec_cd,
                'log_lvl_cd': log_lvl_cd,
                'title': title,
                'from_date': from_date,
                'to_date': to_date,
            }
            logs = service.search_log(param)

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
            writer.writerow(['ログレベル', '年月日', '時刻', '操作端末IP', 'ユーザ名', 'ログ種別', 'ジョブID', 'ジョブタイトル', '内容'])
            # body
            for row in logs:
                writer.writerow([
                    row['log_lvl_name'], 
                    row['output_date'],
                    row['output_time'],
                    row['ope_ip_address'],
                    row['log_output_id'],
                    row['log_type_name'],
                    row['job_id'],
                    row['title'],
                    row['content'],
                ])

            res = make_response()
            res.data = file.getvalue().encode("utf_8_sig")
            res.headers['Content-Type'] = 'text/csv'
            res.headers['Content-Disposition'] = 'attachement; filename=JOBLOG_{}.csv'.format(strdate)
            return res

        except Exception as e:
            print(traceback.format_exc())
            raise e


    def txt_download(self):
        '''
        Txt出力
        '''
        try:
            # parameter
            tec_cd = session['tec_cd']
            user_id = session['user']
            log_lvl_cd = request.form['selectLogLvl']
            title = '%{}%'.format(request.form['jobTitle']) if request.form['jobTitle'] != '' else None
            from_date = request.form['fromDate']
            to_date = request.form['toDate']
            sysdate = datetime.now()
            strdate = datetime.strftime(sysdate, '%Y%m%d%H%M%S')

            # ホスト名・IPアドレス取得
            # host = socket.gethostname()
            # ip_address = socket.gethostbyname(host)
            ip_address = request.remote_addr

            # Service instanced
            service = LogService()

            param = {
                'tec_cd': tec_cd,
                'log_lvl_cd': log_lvl_cd,
                'title': title,
                'from_date': from_date,
                'to_date': to_date,
            }
            logs = service.search_log(param)

            # ログ登録
            log_param = {
                'tec_cd': tec_cd,
                'log_output_timestamp': sysdate,
                'log_output_id': user_id,
                'log_type_cd': '017', # 017:テキストファイル出力
                'job_id': None,
                'error_content': None,
                'ope_ip_address': ip_address,
            }
            service.insert_log(log_param)

            file = StringIO()
            writer = csv.writer(file, delimiter=' ', quoting=csv.QUOTE_NONE)

            # header
            writer.writerow(['ログレベル', '年月日', '時刻', '操作端末IP', 'ユーザ名', 'ログ種別', 'ジョブID', 'ジョブタイトル', '内容'])
            # body
            for row in logs:
                writer.writerow([
                    row['log_lvl_name'], 
                    row['output_date'],
                    row['output_time'],
                    row['ope_ip_address'],
                    row['log_output_id'],
                    row['log_type_name'],
                    row['job_id'],
                    row['title'],
                    row['content'],
                ])

            res = make_response()
            res.data = file.getvalue().encode("utf_8_sig")
            res.headers['Content-Type'] = 'text/plain'
            res.headers['Content-Disposition'] = 'attachement; filename=JOBLOG_{}.txt'.format(strdate)
            return res

        except Exception as e:
            print(traceback.format_exc())
            raise e