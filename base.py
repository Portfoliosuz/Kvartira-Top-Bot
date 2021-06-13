import sqlite3
def createtable(name):
    conn = sqlite3.connect('data.db')

    baza = conn.cursor()

    baza.execute(
        f"""
        create table if not exists {name}(
        ism text,
        id text,
        username text,
        tel text,
        latitude text,
        longitude text,
        izoh text
        
        ) 
    """)

    conn.commit()
    conn.close()


def add(name,ism,id,username,tel,latitude,longitude,izoh):
    conn = sqlite3.connect('data.db')

    baza = conn.cursor()

    baza.execute(
        f"""
        insert into'{name}' values(
        '{ism}',
        '{id}',
        '@{username}',
        '{tel}',
        '{latitude}',
        '{longitude}',
        '{izoh}' 
        ) 
    """)
    conn.commit()
    conn.close()
def delete(name,ism,id,username,tel,latitude,longitude,izoh):
    conn = sqlite3.connect('data.db')

    baza = conn.cursor()

    baza.execute(
        f"""
        delete from {name} where id = {id} and  latitude={latitude} and longitude={longitude}
    """)
    conn.commit()
    conn.close()
def addusers(id,ism,username,tel):
    conn = sqlite3.connect('data.db')

    baza = conn.cursor()

    baza.execute(
        f"""
        insert into users values(
        '{ism}',
        '{id}',
        '@{username}' ,
        '{tel}' 
        ) 
    """)

    conn.commit()
    conn.close()
def search_user(id):

    conn = sqlite3.connect('data.db')

    baza = conn.cursor()

    baza=baza.execute(
        f"""
        select * from users where id={id}
    """).fetchall()
    return baza
    conn.commit()
    conn.close()

def search(name):
    llist = []
    conn = sqlite3.connect('data.db')

    baza = conn.cursor()

    baza=baza.execute(
        f"""
        select latitude,longitude from {name}
    """).fetchall()
    for i in baza:
        llist.append([float(i[0]),float(i[1])])
    return llist
    conn.commit()
    conn.close()

def search_place_info(name,lat,long):
    conn = sqlite3.connect('data.db')

    baza = conn.cursor()

    baza=baza.execute(
        f"""
        select * from {name} where latitude = {lat} and longitude  = {long}
    """).fetchall()

    return baza
    conn.commit()
    conn.close()
