import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import auth
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # S tem se znebimo problemov z npr. šumniki

def ustvari_tabele():
    cur.execute("""
        CREATE TABLE zdravstveni_dom (
            id SERIAL PRIMARY KEY,
            naslov TEXT NOT NULL,
            ime TEXT NOT NULL,  
            kapaciteta INTEGER NOT NULL
        );
        
        CREATE TABLE zdravnik (
            emso TEXT PRIMARY KEY,
            ime TEXT NOT NULL,
            priimek TEXT NOT NULL,
            specializacija TEXT NOT NULL,
            datum_rojstva DATE NOT NULL,
            izkusnje TEXT
        );
        
        CREATE TABLE pacient (
            emso TEXT PRIMARY KEY,
            zdravstvena_st INTEGER NOT NULL,
            ime TEXT NOT NULL,
            priimek TEXT NOT NULL,
            spol CHAR(1) NOT NULL,
            datum_rojstva DATE NOT NULL,
            teza DECIMAL,
            visina DECIMAL,
            zdravnik_emso TEXT REFERENCES zdravnik(emso)
        );
        
        CREATE TABLE zaposlitev (
            zdravnik_emso TEXT REFERENCES zdravnik(emso),
            zdravstveni_dom_id INTEGER REFERENCES zdravstveni_dom(id),
            datum DATE NOT NULL,
            PRIMARY KEY (zdravnik_emso, zdravstveni_dom_id)
        );
        
        CREATE TABLE pregled (
            pacient_emso TEXT NOT NULL REFERENCES pacient(emso),
            datum TIMESTAMP NOT NULL,
            zdravstveni_dom_id INTEGER REFERENCES zdravstveni_dom(id),
            zdravnik_emso TEXT NOT NULL REFERENCES zdravnik(emso),
            razlog TEXT,
            izvid TEXT,
            PRIMARY KEY (pacient_emso, datum)
        );
        
        CREATE TABLE sporocilo (
            pacient_emso TEXT NOT NULL REFERENCES pacient(emso),
            datum TIMESTAMP NOT NULL,
            zdravnik_emso TEXT NOT NULL REFERENCES zdravnik(emso),
            nujnost TEXT NOT NULL,
            tema TEXT,
            vsebina TEXT NOT NULL,
            PRIMARY KEY (pacient_emso, datum)
        );

        CREATE TABLE uporabnik_pacient (
            emso TEXT PRIMARY KEY REFERENCES pacient(emso),
            uporabnisko_ime TEXT NOT NULL,
            geslo TEXT NOT NULL  
        );

        CREATE TABLE uporabnik_zdravnik (
            emso TEXT PRIMARY KEY REFERENCES zdravnik(emso),
            uporabnisko_ime TEXT NOT NULL,
            geslo TEXT NOT NULL  
        );
    """)
    conn.commit()

def pobrisi_tabele():
    cur.execute("""
        DROP TABLE uporabnik_pacient;
        DROP TABLE uporabnik_zdravnik;
        DROP TABLE sporocilo;
        DROP TABLE pregled;
        DROP TABLE zaposlitev;
        DROP TABLE pacient;
        DROP TABLE zdravnik;
        DROP TABLE zdravstveni_dom;
    """)
    conn.commit()

def uvozi_podatke():
    for ime_dat in ["zdravstveni_dom.sql", "zdravnik.sql", "pacient.sql", "zaposlitev.sql", "pregled.sql", "sporocilo.sql", "uporabnik_pacient.sql", "uporabnik_zdravnik.sql"]:
        with open(os.path.join(current, "podatki", ime_dat)) as d:
            cur.execute(d.read())
            conn.commit()

def resetiraj_bazo():
    pobrisi_tabele()
    ustvari_tabele()
    uvozi_podatke()

# Test interakcije z online bazo:
def zdravstveni_dom(stevilo=100):
    cur.execute("""
        SELECT id, naslov, ime, kapaciteta FROM zdravstveni_dom
        WHERE kapaciteta >= %s
    """, [stevilo])
    for id, naslov, ime, kapaciteta in cur:
        print(f"Zdravstveni dom {ime} na naslovu {naslov} z IDjem {id} ima kapaciteto {kapaciteta}")

conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 