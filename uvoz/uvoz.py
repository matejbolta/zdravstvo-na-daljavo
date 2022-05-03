from . import auth

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

def ustvari_tabele():
    cur.execute("""
        CREATE TABLE zdravstveni_dom (
        id SERIAL PRIMARY KEY,
        naslov TEXT NOT NULL,
        ime TEXT NOT NULL,
        kapaciteta INTEGER
        );
        
        CREATE TABLE zdravnik (
        emšo INT PRIMARY KEY,
        ime TEXT NOT NULL,
        priimek TEXT NOT NULL,
        specializacija TEXT NOT NULL,
        datum_rojstva DATE NOT NULL,
        izkusnje TEXT
        );
        
        CREATE TABLE pacient (
        emšo INTEGER PRIMARY KEY,
        zdravstvena_št INTEGER NOT NULL,
        ime TEXT NOT NULL,
        priimek TEXT NOT NULL,
        spol CHAR(1) NOT NULL,
        datum_rojstva DATE NOT NULL,
        teža DECIMAL,
        višina DECIMAL,
        osebni_zdravnik INTEGER REFERENCES zdravnik(emšo)
        );
        
        CREATE TABLE zaposlitev (
        zdravnik INTEGER REFERENCES zdravnik(emšo),
        zdravstveni_dom INTEGER REFERENCES zdravstveni_dom(id),
        datum_zaposlitve DATE NOT NULL,
        PRIMARY KEY (zdravnik, zdravstveni_dom)
        );
        
        CREATE TABLE pregled (
        pacient INTEGER NOT NULL REFERENCES pacient(emšo),
        čas TIMESTAMP NOT NULL,
        zdravstveni_dom INTEGER REFERENCES zdravstveni_dom(id),
        zdravnik INTEGER NOT NULL REFERENCES zdravnik(emšo),
        razlog TEXT,
        izvid TEXT,
        PRIMARY KEY (pacient, čas)
        );
        
        CREATE TABLE sporocilo (
        pacient INTEGER NOT NULL REFERENCES pacient(emšo),
        čas TIMESTAMP NOT NULL,
        zdravnik INTEGER NOT NULL REFERENCES zdravnik(emšo),
        nujnost TEXT NOT NULL,
        tema TEXT,
        vsebina TEXT NOT NULL,
        PRIMARY KEY (pacient, čas)
        );
    """)
    conn.commit()

def pobrisi_tabele():
    cur.execute("""
        DROP TABLE sporocilo;
        DROP TABLE pregled;
        DROP TABLE zaposlitev;
        DROP TABLE pacient;
        DROP TABLE zdravnik;
        DROP TABLE zdravstveni_dom;
    """)
    conn.commit()

conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
