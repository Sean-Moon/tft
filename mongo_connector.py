import pymongo

class MongoConnector:
    def __init__(self):
        self.conn = pymongo.MongoClient('mongodb://root:root@220.90.208.81:27017/root?authSource=root')
        #self.db = conn.root # AAA라는 이름의 데이터베이스 생성
        #collection  = db.korbit # test라는 이름의 테이블 생성
        self.db = self.conn.get_database('root') # 데이터베이스 선택
        self.collection = self.db.get_collection('korbit') # 테이블 선택
    def insertData(self,_collected):
        ## 예시
        self.collection.insert(_collected) # 선택된 컬렉션에 키가 number, 값이 0인 데이터 저장
    def close(self):
        self.conn.close()