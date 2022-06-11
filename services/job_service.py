import configparser
import os
import pathlib
import psycopg2.extensions
from helpers.db_helper import PostgreConnect

class JobService:
    '''
    ジョブ画面のサービスクラス
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
            sql += "   , COALESCE(TJS.content, '')           AS content "
            sql += "   , COALESCE(TJS.result_content, '')    AS result_content "
            sql += "   , TJS.progress                        AS progress "
            sql += "   , TJS.job_status_cd                   AS job_status_cd"
            sql += "   , MJS.job_status_name                 AS job_status_name "
            sql += "   , TO_CHAR(TJS.use_bcast_timestamp,'YYYY/MM/DD HH24:MI')  AS use_bcast_timestamp "
            sql += "   , TJS.modified_timestamp              AS modified_timestamp "
            sql += " FROM "
            sql += "   tbl_job_status TJS "
            sql += " INNER JOIN mst_job_status MJS "
            sql += "   ON TJS.tec_cd = MJS.tec_cd "
            sql += "  AND TJS.job_status_cd = MJS.job_status_cd "
            sql += " WHERE 1 = 1 "
            sql += "   AND TJS.tec_cd = %(tec_cd)s "
            sql += "   AND TJS.job_id = %(job_id)s "

            # SQL実行
            res = self.db.execute_scalor_dict(sql, param)
            return res

        except Exception as e:
            raise e


    def get_loop_machine(self, param):
        '''
        ループ構成機器情報取得
        '''
        try:
            res = None

            sql  = " SELECT "
            sql += "   ip_address "
            sql += "   , if_name "
            sql += "   , COALESCE(hostname, '')       AS hostname "
            sql += "   , COALESCE(machine_type, '')   AS machine_type "
            sql += "   , vlan_id "
            sql += "   , macflap_count_per_min "
            sql += "   , COALESCE(location, '')       AS location "
            sql += "   , COALESCE(rack_location, '')  AS rack_location "
            sql += "   , COALESCE(nw_type, '')        AS nw_type "
            sql += "   , COALESCE(loop_flag, False)   AS loop_flag "
            sql += " FROM "
            sql += "   tbl_loop_machine "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "
            sql += "   AND job_id = %(job_id)s "
            sql += " ORDER BY "
            sql += "   loop_flag DESC, hostname "

            # SQL実行
            res = self.db.execute_query_dict(sql, param)
            return res

        except Exception as e:
            raise e


    def get_unable_connect(self, param):
        '''
        機器接続不可情報取得
        '''
        try:
            res = None

            sql  = " SELECT "
            sql += "   ip_address "
            sql += "   , COALESCE(hostname, '')        AS hostname "
            sql += "   , COALESCE(connect_method, '')  AS connect_method "
            sql += "   , COALESCE(error_content, '')   AS error_content "
            sql += " FROM "
            sql += "   tbl_unable_connect "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "
            sql += "   AND job_id = %(job_id)s "

            # SQL実行
            res = self.db.execute_query_dict(sql, param)
            return res

        except Exception as e:
            raise e


    def get_job_edit(self, param):
        '''
        ジョブ編集情報取得
        '''
        try:
            res = None

            sql  = " SELECT "
            sql += "   job_id "
            sql += "   , COALESCE(title, '')                        AS title "
            sql += "   , COALESCE(create_user_name, '')             AS create_user_name "
            sql += "   , COALESCE(content, '')                      AS content "
            sql += "   , TO_CHAR(use_bcast_timestamp,'YYYY/MM/DD')  AS bcast_data_date "
            sql += "   , TO_CHAR(use_bcast_timestamp,'HH24:MI')     AS bcast_data_time "
            sql += "   , modified_timestamp "
            sql += " FROM "
            sql += "   tbl_job_status "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "
            sql += "   AND job_id = %(job_id)s "

            # SQL実行
            res = self.db.execute_scalor_dict(sql, param)
            return res

        except Exception as e:
            raise e


    def get_auto_count(self, param):
        '''
        自動実行中ジョブ件数取得
        '''
        try:
            res = None

            sql  = " SELECT "
            sql += "   COUNT(1) AS JOB_COUNT "
            sql += " FROM "
            sql += "   tbl_job_status "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "
            sql += "   AND job_status_cd = %(job_status_cd)s "
            sql += "   AND create_user_name = %(create_user_name)s "
            sql += "   AND del_flg = %(del_flg)s "

            # SQL実行
            res = self.db.execute_scalor_dict(sql, param)
            return int(res['job_count']) if res != None else 0

        except Exception as e:
            raise e


    def insert_log_csv(self, param):
        '''
        ログテーブル登録
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
            res = self.db.execute(sql, param)
            return res

        except Exception as e:
            raise e


    def get_job_id(self, param, cur: psycopg2.extensions.cursor):
        '''
        新規ジョブID取得
        '''
        try:
            sql  = " SELECT "
            sql += "   CAST(CAST(job_id as integer) + 1 as text) AS job_id "
            sql += " FROM "
            sql += "   tbl_job_id "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "

            # SQL実行
            cur.execute(sql, param)
            res = cur.fetchone()
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
            res = cur.fetchone()
            return res

        except Exception as e:
            raise e


    def update_job_termination(self, param, cur: psycopg2.extensions.cursor):
        '''
        ジョブ実行状態テーブル更新(強制終了)
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
            # res = self.db.execute(sql, param)
            res = cur.execute(sql, param)
            return res

        except Exception as e:
            raise e


    def update_job_status(self, param, cur: psycopg2.extensions.cursor):
        '''
        ジョブ実行状態テーブル更新
        '''
        try:
            sql  = " UPDATE tbl_job_status SET "
            sql += "   title = %(title)s "
            sql += "   , create_user_name = %(create_user_name)s "
            sql += "   , content = %(content)s "
            sql += "   , ope_ip_address = %(ope_ip_address)s "
            sql += "   , modified_timestamp = %(modified_timestamp)s "
            sql += "   , modified_user_id = %(modified_user_id)s "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "
            sql += "   AND job_id = %(job_id)s "

            # SQL実行
            # res = self.db.execute(sql, param)
            res = cur.execute(sql, param)
            return res

        except Exception as e:
            raise e


    def update_job_id(self, param, cur: psycopg2.extensions.cursor):
        '''
        ジョブID管理テーブル更新
        '''
        try:
            sql  = " UPDATE tbl_job_id SET "
            sql += "   job_id = %(job_id)s "
            sql += "   , ope_ip_address = %(ope_ip_address)s "
            sql += "   , modified_timestamp = %(modified_timestamp)s "
            sql += "   , modified_user_id = %(modified_user_id)s "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "

            # SQL実行
            res = cur.execute(sql, param)
            return res

        except Exception as e:
            raise e


    def insert_job_id(self, param, cur: psycopg2.extensions.cursor):
        '''
        ジョブID管理テーブル登録
        '''
        try:
            sql  = " INSERT INTO "
            sql += " tbl_job_id( "
            sql += "   tec_cd "
            sql += "   , job_id "
            sql += "   , ope_ip_address "
            sql += "   , created_timestamp "
            sql += "   , created_user_id "
            sql += "   , modified_timestamp "
            sql += "   , modified_user_id "
            sql += " ) "
            sql += " VALUES( "
            sql += "   %(tec_cd)s "
            sql += "   , %(job_id)s "
            sql += "   , %(ope_ip_address)s "
            sql += "   , %(created_timestamp)s "
            sql += "   , %(created_user_id)s "
            sql += "   , %(modified_timestamp)s "
            sql += "   , %(modified_user_id)s "
            sql += " ) "

            # SQL実行
            res = cur.execute(sql, param)
            return res

        except Exception as e:
            raise e


    def insert_job(self, param, cur: psycopg2.extensions.cursor):
        '''
        ジョブ実行状態テーブル登録
        '''
        try:
            sql  = " INSERT INTO "
            sql += " tbl_job_status( "
            sql += "   tec_cd "
            sql += "   , job_id "
            sql += "   , job_status_cd "
            sql += "   , title "
            sql += "   , create_user_name "
            sql += "   , content "
            sql += "   , use_bcast_timestamp "
            sql += "   , start_timestamp "
            sql += "   , end_timestamp "
            sql += "   , progress "
            sql += "   , ope_ip_address "
            sql += "   , del_flg "
            sql += "   , created_timestamp "
            sql += "   , created_user_id "
            sql += "   , modified_timestamp "
            sql += "   , modified_user_id "
            sql += " ) "
            sql += " VALUES( "
            sql += "   %(tec_cd)s "
            sql += "   , %(job_id)s "
            sql += "   , %(job_status_cd)s "
            sql += "   , %(title)s "
            sql += "   , %(create_user_name)s "
            sql += "   , %(content)s "
            sql += "   , %(use_bcast_timestamp)s "
            sql += "   , %(start_timestamp)s "
            sql += "   , %(end_timestamp)s "
            sql += "   , %(progress)s "
            sql += "   , %(ope_ip_address)s "
            sql += "   , %(del_flg)s "
            sql += "   , %(created_timestamp)s "
            sql += "   , %(created_user_id)s "
            sql += "   , %(modified_timestamp)s "
            sql += "   , %(modified_user_id)s "
            sql += " ) "

            # SQL実行
            res = cur.execute(sql, param)
            return res

        except Exception as e:
            raise e


    def insert_log(self, param, cur: psycopg2.extensions.cursor):
        '''
        ログテーブル登録
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
            # res = self.db.execute(sql, param)
            res = cur.execute(sql, param)
            return res

        except Exception as e:
            raise e