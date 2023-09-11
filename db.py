import sqlite3
class DB:
    def __init__(self) -> None:
        self.db = sqlite3.connect("database.db")
        try:
            self.db.execute('''CREATE TABLE DOWNLOADED
                    (URL       TEXT    PRIMARY KEY NOT NULL,
                    THUMB_URL  TEXT    NOT NULL,
                    TITLE      TEXT    NOT NULL);''')
        except Exception as e:
            print(e)
        
        try:
            self.db.execute('''CREATE TABLE DOWNLOAD_QUEUE
                    (URL       TEXT    PRIMARY KEY NOT NULL
                    );''')
        except Exception as e:
            print(e)
            
    def queue_pull(self):
        try:
            curs = self.db.execute(f'''
                    SELECT * FROM DOWNLOAD_QUEUE
                    LIMIT 1;
                    ''')
            row = curs.fetchone()
            if row:
                url = row[0]
                return url
            else:
                return False
        except Exception as e:
            print(e)
        
    def queue_insert(self, url):
        try:
            self.db.execute(f'''
                    INSERT INTO DOWNLOAD_QUEUE
                    (URL) 
                    VALUES 
                    ("{url}");
                    ''')
            self.db.commit()
        except Exception as e:
            print(e)
            
            
    def queue_delete(self,url):
        try:
            self.db.execute(f'''
                    DELETE FROM DOWNLOAD_QUEUE
                    WHERE 
                    URL = "{url}";
                    ''')
            self.db.commit()
        except Exception as e:
            print(e)
            
            
    def queue_clear(self):
        try:
            self.db.execute(f'''
                    DELETE FROM DOWNLOAD_QUEUE;
                    ''')
            self.db.commit()
            self.db.execute(f'''
                    VACUUM;
                    ''')
        except Exception as e:
            print(e)
            
            
    def dl_complete(self, url):
        try:
            self.db.execute(f'''
                    INSERT INTO DOWNLOADED
                    (URL, THUMB_URL, TITLE) 
                    VALUES 
                    ("{url}","None","None");
                    ''')
            self.db.commit()
        except Exception as e:
            print(e)
            
    def dl_check_history(self,url):
        try:
            curs = self.db.execute(f'SELECT URL FROM DOWNLOADED WHERE URL="{url}";')
            result = curs.fetchone()
            if result is None:
                return False
            else:
                return True
        except Exception as e:
            print(e)
            
    def dl_get_queue(self):
        try:
            curs = self.db.execute(f'SELECT * FROM DOWNLOAD_QUEUE;')
            result = curs.fetchall()
            if result is None:
                return False
            else:
                return result
        except Exception as e:
            print(e)