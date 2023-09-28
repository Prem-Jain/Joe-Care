import sqlite3
class ExpertRequest:
    def add_expert(userid, name, email, phno, msg, res, req):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            x = (userid, name, email, phno, msg, res, req)
            insert = """INSERT INTO expert (userid, name, email, phno, msg, res, req) VALUES (?,?,?,?,?,?,?);"""
            c.execute(insert, x)
        finally:
            con.commit()
            c.close()
            con.close()
        
    def get_expert_req():
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            sql_select_query = "select * from expert where req = ?;"
            c.execute(sql_select_query, ("False",))
            record = c.fetchall()
        finally:
            con.commit()
            c.close()
            con.close()
        return record