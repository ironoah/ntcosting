import configparser
import os
import pathlib
from helpers.db_helper import PostgreConnect

class LogService:
    '''
    ログ画面のサービスクラス
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


    def get_log(self, param):
        '''
        ジョブ情報取得
        '''
        try:
            res = None

            sql  = " SELECT "
            sql += "   MLL.log_lvl_name                                 AS log_lvl_name "
            sql += "   , TO_CHAR(TL.log_output_timestamp,'YYYY/MM/DD')  AS output_date "
            sql += "   , TO_CHAR(TL.log_output_timestamp,'HH24:MI')     AS output_time "
            sql += "   , COALESCE(TL.ope_ip_address, '')                AS ope_ip_address "
            sql += "   , COALESCE(TL.log_output_id, '')                 AS log_output_id "
            sql += "   , COALESCE(MLT.log_type_name, '')                AS log_type_name "
            sql += "   , COALESCE(TL.job_id, '')                        AS job_id "
            sql += "   , COALESCE(TJS.title, '')                        AS title "
            sql += "   , COALESCE(TJS.content,'')                       AS content "
            sql += " FROM "
            sql += "   tbl_log TL "
            sql += " INNER JOIN mst_log_type MLT "
            sql += "   ON TL.tec_cd = MLT.tec_cd "
            sql += "  AND TL.log_type_cd = MLT.log_type_cd "
            sql += " INNER JOIN mst_log_lvl MLL "
            sql += "   ON MLT.tec_cd = MLL.tec_cd "
            sql += "  AND MLT.log_lvl_cd = MLL.log_lvl_cd "
            sql += " LEFT JOIN tbl_job_status TJS "
            sql += "   ON TL.tec_cd = TJS.tec_cd "
            sql += "  AND TL.job_id = TJS.job_id "
            sql += " WHERE 1 = 1 "
            sql += "   AND TL.tec_cd = %(tec_cd)s "
            sql += "   AND TL.log_output_timestamp BETWEEN CURRENT_DATE + CAST('00:00:00' as time) AND CURRENT_DATE + CAST('23:59:59' as time) "
            sql += " ORDER BY "
            sql += "   TL.log_output_timestamp DESC "

            # SQL実行
            res = self.db.execute_query_dict(sql, param)
            return res

        except Exception as e:
            raise e


    def search_log(self, param):
        '''
        ジョブ情報検索
        '''
        try:
            res = None

            sql  = " SELECT "
            sql += "   MLL.log_lvl_name                                 AS log_lvl_name "
            sql += "   , TO_CHAR(TL.log_output_timestamp,'YYYY/MM/DD')  AS output_date "
            sql += "   , TO_CHAR(TL.log_output_timestamp,'HH24:MI')     AS output_time "
            sql += "   , COALESCE(TL.ope_ip_address, '')                AS ope_ip_address "
            sql += "   , COALESCE(TL.log_output_id, '')                 AS log_output_id "
            sql += "   , COALESCE(MLT.log_type_name, '')                AS log_type_name "
            sql += "   , COALESCE(TL.job_id, '')                        AS job_id "
            sql += "   , COALESCE(TJS.title, '')                        AS title "
            sql += "   , REGEXP_REPLACE(COALESCE(TJS.content,''),'\r|\n|\r\n','','g')  AS content "
            sql += " FROM "
            sql += "   tbl_log TL "
            sql += " INNER JOIN mst_log_type MLT "
            sql += "   ON TL.tec_cd = MLT.tec_cd "
            sql += "  AND TL.log_type_cd = MLT.log_type_cd "
            sql += " INNER JOIN mst_log_lvl MLL "
            sql += "   ON MLT.tec_cd = MLL.tec_cd "
            sql += "  AND MLT.log_lvl_cd = MLL.log_lvl_cd "
            sql += " LEFT JOIN tbl_job_status TJS "
            sql += "   ON TL.tec_cd = TJS.tec_cd "
            sql += "  AND TL.job_id = TJS.job_id "
            sql += " WHERE 1 = 1 "
            sql += "   AND TL.tec_cd = %(tec_cd)s "
            if param['log_lvl_cd'] is not None and param['log_lvl_cd'] != '000':
                sql += "   AND MLL.log_lvl_cd = %(log_lvl_cd)s "
            if param['title'] is not None and param['title'] != '':
                sql += "   AND TJS.title LIKE %(title)s "
            sql += "   AND TL.log_output_timestamp BETWEEN CAST(%(from_date)s as date) + CAST('00:00:00' as time) AND CAST(%(to_date)s as date) + CAST('23:59:59' as time) "
            sql += " ORDER BY "
            sql += "   TL.log_output_timestamp DESC "

            # SQL実行
            res = self.db.execute_query_dict(sql, param)
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