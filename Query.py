import sqlite3
class Query:
    def add_new_post(userid, title, desc, anony, name, email, age):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            x = (userid, title, desc, anony, name, email, age, "True", "False", "False")
            insert = """INSERT INTO ApprovePosts (userid, title, desc, anonymous, name, email, age, mod, app, ageres) VALUES (?,?,?,?,?,?,?,?,?,?);"""
            c.execute(insert, x)
        finally:
            con.commit()
            c.close()
            con.close()

    def get_app_post():
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            sql_select_query = "select * from approvePosts where app = 'True' order by id desc;"
            c.execute(sql_select_query)
            record = c.fetchall()
        finally:
            con.commit()
            c.close()
            con.close()
        return record

    def get_post_postid(postid):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            sql_select_query = "select * from approvePosts where id = ?;"
            c.execute(sql_select_query, (postid,))
            record = c.fetchall()
        finally:
            con.commit()
            c.close()
            con.close()
        return record

    def add_comment(postid, userid, name, email, comment, anony):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            x = (postid, userid, name, email, comment, anony)
            insert = """INSERT INTO comments (postid, userid, user, email, comment, anony) VALUES (?,?,?,?,?,?);"""
            c.execute(insert, x)
        finally:
            con.commit()
            c.close()
            con.close()
        
    def get_comments(postid):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            sql_select_query = "select * from comments where postid = ?;"
            c.execute(sql_select_query, (postid,))
            record = c.fetchall()
        finally:
            con.commit()
            c.close()
            con.close()
        return record
    
    def get_posts_profile(userid):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            sql_select_query = "select * from approvePosts where userid = ? order by id desc;"
            c.execute(sql_select_query, (userid,))
            record = c.fetchall()
        finally:
            con.commit()
            c.close()
            con.close()
        return record


            
    def update_post(title, desc, anony, postid):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            x = (title, desc, anony, "True", "False", postid)
            update = "UPDATE ApprovePosts SET title = ?, desc = ?, anonymous = ?, mod = ?, app = ? WHERE id = ?;"
            c.execute(update, x)
        finally:
            con.commit()
            c.close()
            con.close()
            
    def delete_query(postid):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            delete = "DELETE FROM ApprovePosts WHERE id = ?;"
            c.execute(delete, (postid,))
        finally:
            con.commit()
            c.close()
            con.close()