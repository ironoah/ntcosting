import configparser
import os
import pathlib
import psycopg2.extensions
from helpers.db_helper import PostgreConnect

class TopService:
    '''
    TOP画面のサービスクラス
    '''
    def __init__(self):
        '''
        コンストラクタ
        '''
        path = os.path.join(pathlib.Path(os.path.dirname(__file__)).parent, 'config.ini')
        config = configparser.ConfigParser()
        config.read(path, 'utf_8_sig')
        db_conn = config['db_connection']
        self.db = PostgreConnect(db_conn['DB_HOST'], db_conn['DB_NAME'], db_conn['DB_SCHEME'], db_conn['DB_USER'], db_conn['DB_PASS'], db_conn['DB_PORT'])


    def get_job(self, param):
        '''
        ジョブ情報取得
        '''
        try:
            res = None

            sql  = " SELECT "
            sql += "   TJS.job_id                            AS job_id "
            sql += "   , COALESCE(TJS.title, '')             AS title "
            sql += "   , COALESCE(TJS.create_user_name, '')  AS create_user_name "
            sql += "   , TO_CHAR(TJS.start_timestamp,'YYYY/MM/DD HH24:MI:SS')  AS start_timestamp "
            sql += "   , TJS.job_status_cd       AS job_status_cd"
            sql += "   , MJS.job_status_name     AS job_status_name "
            sql += "   , TJS.progress            AS progress "
            sql += "   , TJS.modified_timestamp  AS modified_timestamp "
            sql += " FROM "
            sql += "   tbl_job_status TJS "
            sql += " INNER JOIN mst_job_status MJS "
            sql += "   ON TJS.tec_cd = MJS.tec_cd "
            sql += "  AND TJS.job_status_cd = MJS.job_status_cd "
            sql += " WHERE 1 = 1 "
            sql += "   AND TJS.tec_cd = %(tec_cd)s "
            sql += "   AND TJS.start_timestamp BETWEEN CAST(%(from_date)s as date) + CAST('00:00:00' as time) AND CAST(%(to_date)s as date) + CAST('23:59:59' as time) "
            sql += "   AND TJS.del_flg = '0' "
            sql += " ORDER BY "
            sql += "   TJS.start_timestamp DESC "

            # SQL実行
            res = self.db.execute_query_dict(sql, param)
            return res

        except Exception as e:
            raise e


    def get_jobcount(self, param):
        '''
        実行中ジョブ件数取得
        '''
        try:
            res = None

            sql  = " SELECT "
            sql += "   COUNT(1) AS JOB_COUNT "
            sql += " FROM "
            sql += "   tbl_job_status "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "
            sql += "   AND job_status_cd = '010' "
            sql += "   AND del_flg = '0' "

            # SQL実行
            res = self.db.execute_scalor_dict(sql, param)
            return res

        except Exception as e:
            raise e


    def get_jos_status_cd(self, param, cur: psycopg2.extensions.cursor):
        '''
        ジョブステータス取得
        '''
        try:
            sql  = " SELECT "
            sql += "    job_status_cd "
            sql += " FROM "
            sql += "   tbl_job_status "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "
            sql += "   AND job_id = %(job_id)s "
            sql += "   AND del_flg = '0' "

            # SQL実行
            cur.execute(sql, param)
            return cur.fetchone()

        except Exception as e:
            raise e


    def get_latset_date(self, param, cur: psycopg2.extensions.cursor):
        '''
        最新更新日時取得
        '''
        try:
            sql  = " SELECT "
            sql += "   TO_CHAR(modified_timestamp,'YYYY-MM-DD HH24:MI:SS')  AS modified_timestamp "
            sql += " FROM "
            sql += "   tbl_job_status "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "
            sql += "   AND job_id = %(job_id)s "

            # SQL実行
            cur.execute(sql, param)
            return cur.fetchone()

        except Exception as e:
            raise e


    def insert_log(self, param, cur: psycopg2.extensions.cursor):
        '''
        ログ登録
        '''
        try:
            sql  = " INSERT INTO "
            sql += " tbl_log( "
            sql += "   tec_cd "
            sql += "   , log_output_timestamp "
            sql += "   , log_output_id "
            sql += "   , log_type_cd "
            sql += "   , job_id "
            sql += "   , error_content "
            sql += "   , ope_ip_address "
            sql += " ) "
            sql += " VALUES( "
            sql += "   %(tec_cd)s "
            sql += "   , %(log_output_timestamp)s "
            sql += "   , %(log_output_id)s "
            sql += "   , %(log_type_cd)s "
            sql += "   , %(job_id)s "
            sql += "   , %(error_content)s "
            sql += "   , %(ope_ip_address)s "
            sql += " ) "

            # SQL実行
            return cur.execute(sql, param)

        except Exception as e:
            raise e


    def update_job_termination(self, param, cur: psycopg2.extensions.cursor):
        '''
        ジョブ実行状態更新(強制終了)
        '''
        try:
            sql  = " UPDATE tbl_job_status SET "
            sql += "   job_status_cd = %(job_status_cd)s "
            sql += "   , ope_ip_address = %(ope_ip_address)s "
            sql += "   , modified_timestamp = %(modified_timestamp)s "
            sql += "   , modified_user_id = %(modified_user_id)s "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "
            sql += "   AND job_id = %(job_id)s "
            sql += "   AND job_status_cd = %(execution_cd)s "

            # SQL実行
            return cur.execute(sql, param)

        except Exception as e:
            raise e


    def update_job_delete(self, param, cur: psycopg2.extensions.cursor):
        '''
        ジョブ実行状態更新(削除)
        '''
        try:
            sql  = " UPDATE tbl_job_status SET "
            sql += "   del_flg = '1' "
            sql += "   , ope_ip_address = %(ope_ip_address)s "
            sql += "   , modified_timestamp = %(modified_timestamp)s "
            sql += "   , modified_user_id = %(modified_user_id)s "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "
            sql += "   AND job_id = %(job_id)s "

            # SQL実行
            return cur.execute(sql, param)

        except Exception as e:
            raise e