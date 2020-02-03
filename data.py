import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY, company_name text, title_name text, application_date date, application_status text)")
        self.conn.commit()
        
    def fetch(self):
        self.cur.execute("SELECT * FROM applications")
        rows = self.cur.fetchall()
        return rows
        
    def insert(self, company_name, title_name, application_date, application_status):
        self.cur.execute("INSERT INTO applications VALUES (NULL, ?, ?, ?, ?)", (company_name, title_name, application_date, application_status))
        self.conn.commit()
    
    def remove(self, id):
        self.cur.execute("DELETE FROM applications WHERE id=?", (id,))
        self.conn.commit()
        
    def update(self, id, company_name, title_name, application_date, application_status):
        self.cur.execute("UPDATE applications SET company_name = ?, title_name = ?, application_date = ?, application_status = ? WHERE id =?", (company_name, title_name, application_date, application_status, id))
        self.conn.commit()
        
    def count_total(self):
        self.cur.execute("SELECT COUNT() FROM applications")
        active = self.cur.fetchone()[0]
        self.conn.commit()
        return active
        
    def count_active(self):
        self.cur.execute("SELECT COUNT() FROM applications WHERE application_status='Active' ")
        active = self.cur.fetchone()[0]
        self.conn.commit()
        return active
    
    def count_rejected(self):
        self.cur.execute("SELECT COUNT() FROM applications WHERE application_status='Rejected' ")
        rejected = self.cur.fetchone()[0]
        self.conn.commit()
        return rejected
        
    def count_accepted(self):
        self.cur.execute("SELECT COUNT() FROM applications WHERE application_status='Offer Accepted' ")
        accepted = self.cur.fetchone()[0]
        self.conn.commit()
        return accepted
        
    def __del__(self):
        self.conn.close()
        
    # Populate DB with placeholder Data
db = Database('applications.db')

