import sqlite3
class AdminUSER:
    def __init__(self):
        self.status = False
    def set_login(self):
        self.status = True
    def set_logout(self):
        self.status = False
    def get_status(self):
        return self.status
    
class Admin:
    def get_admin():
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            sql_select_query = "select * from adminUsers;"
            c.execute(sql_select_query)
            record = c.fetchall()
        finally:
            con.commit()
            c.close()
            con.close()
        return record

    def get_posts():
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            sql_select_query = "select * from approvePosts where mod = 'True';"
            c.execute(sql_select_query)
            record = c.fetchall()
        finally:
            con.commit()
            c.close()
            con.close()
        return record

    def post_approve(postid, mod, app, ageres):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            x = (mod, app, ageres, postid)
            update = "UPDATE ApprovePosts SET mod = ?, app = ?, ageres = ? WHERE id = ?;"
            c.execute(update, x)
        finally:
            con.commit()
            c.close()
            con.close()
        
    def req_completed(reqid, done):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            x = (done, reqid)
            update = "UPDATE expert SET req = ? WHERE id = ?;"
            c.execute(update, x)
        finally:
            con.commit()
            c.close()
            con.close()