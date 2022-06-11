import psycopg2
import psycopg2.extras
 
class PostgreConnect:
    '''
    PostgreSQのヘルパークラス
    '''
 
    def __init__(self, host, dbname, scheme, user, password, port=5432):
        '''
        DBの接続情報を保持する
        Parameters
        ----------
        host : str
            ホスト名
        dbname : str
            DB名
        scheme : str
            スキーマ名
        user : str
            ユーザー名
        password : str
            パスワード
        port : integer
            ポート
        '''
        self.host = host
        self.dbname = dbname
        self.scheme = scheme
        self.user = user
        self.password = password
        self.port = port
    
    def __connect(self):
        return psycopg2.connect("host='{0}' port={1} dbname={2} user={3} password='{4}'".format(self.host, self.port, self.dbname, self.user, self.password))

    def execute_query_dict(self, sql, param):
        '''
        select 系のSQLを実行し、結果を全て取得する
        Parameters
        ----------
        columns : str
            実行したいSQL
        Returns
        ----------
        data: list
            １行分をタプルとし、複数行をリストとして返す
            <例> [('RX100','tani',35000),('RX200','tani',42000)]
        '''
        res = []
        conn = self.__connect()
        conn.cursor_factory = psycopg2.extras.DictCursor
        cur = conn.cursor()
        cur.execute(sql,param)
        data = cur.fetchall()
        for row in data:
            res.append(dict(row))

        cur.close()
        conn.close()
        return res

    def execute_scalor_dict(self, sql, param):
        '''
        結果の値が１つしかないSQLを実行し、結果を取得する
        Parameters
        ----------
        columns : str
            実行したいSQL
        Returns
        ----------
        res:
            実行結果により返された値
        '''
        conn = self.__connect()
        conn.cursor_factory = psycopg2.extras.DictCursor
        cur = conn.cursor()
        cur.execute(sql,param)
        res = cur.fetchone()
        cur.close()
        conn.close()
        return dict(res) if res != None else None

    def execute(self, sql, param):
        '''
        SQLを実行し、結果を取得する
        Parameters
        ----------
        columns : str
            実行したいSQL
        '''
        conn = self.__connect()
        cur = conn.cursor()
        cur.execute(sql, param)
        conn.commit()
        cur.close()
        conn.close()

    def execute_all(self,sqls):
        '''
        複数のSQLをトランザクション配下で実行する
        Parameters
        ----------
        columns : strs
            実行したいSQLのリスト
        '''
        conn = self.__connect()
        cur = conn.cursor()
        try:
            for sql in sqls:
                cur.execute(sql)
            conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
        cur.close()
        conn.close()

    def execute_query(self,sql):
        '''
        select 系のSQLを実行し、結果を全て取得する
        Parameters
        ----------
        columns : str
            実行したいSQL
        Returns
        ----------
        data: list
            １行分をタプルとし、複数行をリストとして返す
            <例> [('RX100','Sony',35000),('RX200','Sony',42000)]
        '''
        conn = self.__connect()
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        conn.close()
        return res

    def execute_scalor(self,sql):
        '''
        結果の値が１つしかないSQLを実行し、結果を取得する
        Parameters
        ----------
        columns : str
            実行したいSQL
        Returns
        ----------
        res:
            実行結果により返された値
        '''
        conn = self.__connect()
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchone()
        cur.close()
        conn.close()
        return res[0] if res != None else None