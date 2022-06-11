import configparser
import os
import pathlib
from helpers.db_helper import PostgreConnect

class LoginService:
    '''
    ログイン画面のサービスクラス
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


    def get_configuration(self, param):
        '''
        設定情報取得
        '''
        try:
            res = None

            sql  = " SELECT "
            sql += "   login_fail_count "
            sql += " FROM "
            sql += "   mst_configuration "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "

            # SQL実行
            res = self.db.execute_scalor_dict(sql, param)
            return res

        except Exception as e:
            raise e


    def get_account(self, param):
        '''
        アカウント情報取得
        '''
        try:
            res = None

            sql  = " SELECT "
            sql += "   account_id "
            sql += "   , password_mod_timestamp "
            sql += "   , password_mod_term "
            sql += "   , job_lines_page "
            sql += "   , default_bcast_time "
            sql += "   , default_job_title "
            sql += "   , log_lines_page "
            sql += "   , login_fail_count "
            sql += " FROM "
            sql += "   mst_configuration "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "
            sql += "   AND account_id = %(account_id)s "
            sql += "   AND password = %(password)s "

            # SQL実行
            res = self.db.execute_scalor_dict(sql, param)
            return res

        except Exception as e:
            raise e


    def get_logincount(self, param):
        '''
        ログイン失敗回数情報取得
        '''
        try:
            res = None

            sql  = " SELECT "
            sql += "   COUNT(1) AS LOGIN_COUNT "
            sql += " FROM "
            sql += "   tbl_log "
            sql += " WHERE 1 = 1 "
            sql += "   AND tec_cd = %(tec_cd)s "
            sql += "   AND log_type_cd = %(log_type_cd)s "
            sql += "   AND log_output_timestamp BETWEEN (CURRENT_TIMESTAMP(0) - interval '1 minutes') AND CURRENT_TIMESTAMP(0) "

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
            sql += "   , error_content "
            sql += "   , ope_ip_address "
            sql += " ) "
            sql += " VALUES( "
            sql += "   %(tec_cd)s "
            sql += "   , %(log_output_timestamp)s "
            sql += "   , %(log_output_id)s "
            sql += "   , %(log_type_cd)s "
            sql += "   , %(error_content)s "
            sql += "   , %(ope_ip_address)s "
            sql += " ) "

            # SQL実行
            res = self.db.execute(sql, param)
            return res

        except Exception as e:
            raise e