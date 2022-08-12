import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import auth
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # S tem se znebimo problemov z npr. šumniki

def ustvari_tabele():
    try:
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

            CREATE VIEW pacient_okrnjen AS SELECT ime, priimek, emso FROM pacient;

            CREATE VIEW zdravnik_okrnjen AS SELECT ime AS zdravnik_ime, priimek AS zdravnik_priimek, emso AS zdravnik_emso FROM zdravnik;
        """)
    except Exception as e:
        conn.rollback()
        print(e)
    conn.commit()

def pobrisi_tabele():
    try:
        cur.execute("""
            DROP TABLE uporabnik_pacient CASCADE;
            DROP TABLE uporabnik_zdravnik CASCADE;
            DROP TABLE sporocilo CASCADE;
            DROP TABLE pregled CASCADE;
            DROP TABLE zaposlitev CASCADE;
            DROP TABLE pacient CASCADE;
            DROP TABLE zdravnik CASCADE;
            DROP TABLE zdravstveni_dom CASCADE;
        """)
    except Exception as e:
        conn.rollback()
        print(e)
    conn.commit()

def uvozi_podatke():
    for ime_dat in ["zdravstveni_dom.sql", "zdravnik.sql", "pacient.sql", "zaposlitev.sql", "pregled.sql", "sporocilo.sql", "uporabnik_pacient.sql", "uporabnik_zdravnik.sql"]:
        with open(os.path.join(current, "podatki", ime_dat)) as d:
            try:
                cur.execute(d.read())
            except Exception as e:
                conn.rollback()
                print(e)
            conn.commit()

def dodeli_pravice():
    try:
        cur.execute("""
            GRANT SELECT ON uporabnik_pacient, uporabnik_zdravnik, sporocilo, pregled, zaposlitev, pacient, zdravnik, zdravstveni_dom, pacient_okrnjen, zdravnik_okrnjen TO javnost;
            GRANT INSERT ON pacient, pregled, sporocilo TO javnost;
        """)
    except Exception as e:
        conn.rollback()
        print(e)
    conn.commit()

def popravi_ustreznost_podatkov():
    try:
        cur.execute("""
            UPDATE sporocilo
            SET pacient_emso = pacient_emso, zdravnik_emso = (
            SELECT zdravnik_emso FROM pacient WHERE emso=pacient_emso
            );

            UPDATE pregled
            SET pacient_emso = pacient_emso, zdravnik_emso = (
            SELECT zdravnik_emso FROM pacient WHERE emso=pacient_emso
            );
        """)
    except Exception as e:
        conn.rollback()
        print(e)
    conn.commit()

def resetiraj_bazo(tudi_pobrisi):
    if tudi_pobrisi:
        pobrisi_tabele()
    ustvari_tabele()
    uvozi_podatke()
    dodeli_pravice()
    popravi_ustreznost_podatkov()

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

bla