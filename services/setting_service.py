import configparser
import os
import pathlib
import psycopg2.extensions
from helpers.db_helper import PostgreConnect

class SettingService:
    '''
    設定画面のサービスクラス
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


    def get_log_lvl(self, param):
        '''
        ログレベル情報取得
        '''
        try:
            res = None

            sql  = " SELECT "
            sql += "   log_lvl_cd "
            sql += "   , log_lvl_name "
            sql += " FROM "
            sql += "   mst_log_lvl "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "
            sql += " ORDER BY "
            sql += "   display_order "

            # SQL実行
            res = self.db.execute_query_dict(sql, param)
            return res

        except Exception as e:
            raise e


    def get_setting(self, param):
        '''
        設定情報取得
        '''
        try:
            res = None

            sql  = " SELECT "
            sql += "   MC.job_lines_page "
            sql += "   , MC.data_get_timeout "
            sql += "   , MC.macflap_get_time "
            sql += "   , MC.broadcast_get_time "
            sql += "   , MC.default_bcast_time "
            sql += "   , MC.default_job_title "
            sql += "   , MC.auto_job_title "
            sql += "   , MC.output_log_lvl_cd "
            sql += "   , MC.stock_term "
            sql += "   , MC.log_lines_page "
            sql += "   , MC.login_fail_count "
            sql += "   , MC.regular_job_title "
            sql += "   , MC.regular_execute_cycle "
            sql += "   , TO_CHAR(MC.regular_execute_time,'HH24:MI') AS regular_execute_time "
            sql += "   , MC.from_mail_address "
            sql += "   , MC.to_mail_address "
            sql += "   , MC.password_mod_term "
            sql += "   , MC.account_id "
            sql += "   , MC.modified_timestamp "
            sql += "   , MLL.log_lvl_name "
            sql += " FROM "
            sql += "   mst_configuration MC "
            sql += " INNER JOIN mst_log_lvl MLL "
            sql += "   ON MC.tec_cd = MLL.tec_cd "
            sql += "  AND MC.output_log_lvl_cd = MLL.log_lvl_cd "
            sql += " WHERE 1 = 1 "
            sql += "   AND MC.tec_cd = %(tec_cd)s "

            # SQL実行
            res = self.db.execute_scalor_dict(sql, param)
            return res

        except Exception as e:
            raise e


    def insert_log(self, param):
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


    def get_latset_date(self, param, cur: psycopg2.extensions.cursor):
        '''
        最新更新日時取得
        '''
        try:
            sql  = " SELECT "
            sql += "   TO_CHAR(modified_timestamp,'YYYY-MM-DD HH24:MI:SS')  AS modified_timestamp "
            sql += " FROM "
            sql += "   mst_configuration "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "

            # SQL実行
            cur.execute(sql, param)
            return cur.fetchone()

        except Exception as e:
            raise e


    def get_current_setting(self, param, cur: psycopg2.extensions.cursor):
        '''
        現在設定情報取得
        '''
        try:
            res = None

            sql  = " SELECT "
            sql += "   regular_execute_cycle "
            sql += "   , TO_CHAR(regular_execute_time,'HH24:MI') AS regular_execute_time "
            sql += " FROM "
            sql += "   mst_configuration "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "

            # SQL実行
            cur.execute(sql, param)
            res = cur.fetchone()
            return dict(res) if res != None else None

        except Exception as e:
            raise e


    def get_latset_setting(self, param, cur: psycopg2.extensions.cursor):
        '''
        最新設定情報取得
        '''
        try:
            sql  = " SELECT "
            sql += "   job_lines_page "
            sql += "   , default_bcast_time "
            sql += "   , default_job_title "
            sql += "   , log_lines_page "
            sql += "   , account_id "
            sql += " FROM "
            sql += "   mst_configuration "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "

            # SQL実行
            cur.execute(sql, param)
            res = cur.fetchone()
            return dict(res) if res != None else None

        except Exception as e:
            raise e


    def update_general(self, param, cur: psycopg2.extensions.cursor):
        '''
        一般設定情報更新
        '''
        try:
            sql  = " UPDATE mst_configuration SET "
            sql += "   job_lines_page = %(job_lines_page)s "
            sql += "   , data_get_timeout = %(data_get_timeout)s "
            sql += "   , macflap_get_time = %(macflap_get_time)s "
            sql += "   , broadcast_get_time = %(broadcast_get_time)s "
            sql += "   , default_bcast_time = %(default_bcast_time)s "
            sql += "   , default_job_title = %(default_job_title)s "
            sql += "   , auto_job_title = %(auto_job_title)s "
            sql += "   , output_log_lvl_cd = %(output_log_lvl_cd)s "
            sql += "   , stock_term = %(stock_term)s "
            sql += "   , log_lines_page = %(log_lines_page)s "
            sql += "   , login_fail_count = %(login_fail_count)s "
            sql += "   , password_mod_term = %(password_mod_term)s "
            sql += "   , regular_job_title = %(regular_job_title)s "
            sql += "   , regular_execute_cycle = %(regular_execute_cycle)s "
            sql += "   , regular_execute_time = %(regular_execute_time)s "
            sql += "   , from_mail_address = %(from_mail_address)s "
            sql += "   , to_mail_address = %(to_mail_address)s "
            sql += "   , ope_ip_address = %(ope_ip_address)s "
            sql += "   , modified_timestamp = %(modified_timestamp)s "
            sql += "   , modified_user_id = %(modified_user_id)s "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "

            # SQL実行
            return cur.execute(sql, param)

        except Exception as e:
            raise e


    def update_account(self, param, cur: psycopg2.extensions.cursor):
        '''
        アカウント情報更新
        '''
        try:
            sql  = " UPDATE mst_configuration SET "
            sql += "   account_id = %(account_id)s "
            sql += "   , password = %(password)s "
            sql += "   , password_mod_timestamp = %(password_mod_timestamp)s "
            sql += "   , ope_ip_address = %(ope_ip_address)s "
            sql += "   , modified_timestamp = %(modified_timestamp)s "
            sql += "   , modified_user_id = %(modified_user_id)s "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "

            # SQL実行
            return cur.execute(sql, param)

        except Exception as e:
            raise e


    def delete_regular_execute(self, param, cur: psycopg2.extensions.cursor):
        '''
        定期実行情報削除
        '''
        try:
            sql  = " DELETE FROM tbl_regular_execute "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "
            sql += "   AND created_timestamp <= %(created_timestamp)s "

            # SQL実行
            return cur.execute(sql, param)

        except Exception as e:
            raise e