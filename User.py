import sqlite3
class User:
    def add_new_user(name, dob, address, phno, email, password):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            x = (name, dob, address, phno, email, password)
            insert = """INSERT INTO Users (name, dob, address, phno, email, password) VALUES (?,?,?,?,?,?);"""
            c.execute(insert, x)
        finally:
            con.commit()
            c.close()
            con.close()
            
    def check_email_exists(email):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            sql_select_query = "select * from Users where email = ?;"
            c.execute(sql_select_query, (email,))
            record = c.fetchall()   
        finally:
            con.commit()
            c.close()
            con.close()
        if len(record) == 0:
            return False
        else:
            return True

    def get_user_details(email):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            sql_select_query = "select * from Users where email = ?;"
            c.execute(sql_select_query, (email,))
            record = c.fetchall()
        finally:
            con.commit()
            c.close()
            con.close()
        return record[0]
    
    def update_profile(name, dob, address, phno, email, userid):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            x = (name, dob, address, phno, email, userid)
            update = "UPDATE Users SET name = ?, dob = ?, address = ?, phno = ?, email = ? WHERE id = ?;"
            c.execute(update, x)
        finally:
            con.commit()
            c.close()
            con.close()
            
    def update_password(newpwd, userid):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            x = (newpwd, userid)
            update = "UPDATE Users SET password = ?WHERE id = ?;"
            c.execute(update, x)
        finally:
            con.commit()
            c.close()
            con.close()

    def delete_acc_posts(userid):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            delete = "DELETE FROM ApprovePosts WHERE userid = ?;"
            c.execute(delete, (userid,))
        finally:
            con.commit()
            c.close()
            con.close()

    def delete_acc(postid):
        con = sqlite3.connect("joecare.db")
        c = con.cursor()
        try:
            delete = "DELETE FROM Users WHERE id = ?;"
            c.execute(delete, (postid,))
        finally:
            con.commit()
            c.close()
            con.close()