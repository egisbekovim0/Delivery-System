import sqlite3
from typing import Any
from app.schemas import ShipmentCreate, ShipmentUpdate
from contextlib import contextmanager

class Database:
    def connect_to_db(self):
        print("connection to sqlite database")
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""
            create table if not exists shipment(
                id integer primary key, 
                content text, 
                weight real, 
                status text)
        """)
    
    def create(self, shipment: ShipmentCreate)-> int:
        self.cur.execute("select max(id) from shipment")
        result = self.cur.fetchone()

        new_id = 1 if result[0] is None else result[0] + 1
        
        self.cur.execute("""
            insert into shipment
            values (:id, :content, :weight, :status)
                       """,
                       {
                           "id": new_id,
                           **shipment.model_dump(),
                           "status": "placed"
                       })
        self.conn.commit()

        return new_id
    
    def get(self, id: int)-> dict[str, Any] | None:
        self.cur.execute("""
            select * from shipment
               where id = ?
               """, (id, ))
        row = self.cur.fetchone()

        return {
            
        } 
    
    def update(self, id: int, shipment: ShipmentUpdate):
        self.cur.execute("""
            update shipment set status = :status
            where id = :id            
        """, {
            "id": id,
            **shipment.model_dump()
        })
        self.conn.commit()

        return self.get(id)
    
    def delete(self, id:int):
        self.cur.execute("""
            delete from shipment
                    where id = ?
                    """, (id, ))
        self.conn.commit()

    def close(self):
        print("connection closed")
        self.conn.close()
    
    # def __enter__(self):
    #     print("enter the context")
    #     self.connect_to_db()
    #     self.create_table()
    #     return self
    
    # def __exit__(self, *arg):
    #     print("exiting the context")
    #     self.close()

@contextmanager
def managed_db():
    db = Database()
    print("enter setup")
    db.connect_to_db()
    db.create_table()
    print("exit context")

    yield db
    db.close()

with managed_db() as db:
    print(db.get(1))
    print(db.get(12702))