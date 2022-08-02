#!/usr/bin/python
# -*- encoding: utf-8 -*-

# na novo na bazi:
# - dodane tabele uporabnikov (avtomatsko na uvozu)
# - pravice javnosti (select, insert, update, delete na uporabnik_zdravnik in uporabnik_pacient)

# Uvozimo bottle. Bottleext nam omogoča pravilno lepljenje URLjev, da ne pride to težav pri pogonu iz oblaka (binder)
from numpy import ufunc
from bottleext import get, post, request, url, response, run, template, redirect, static_file, debug

# Na bazo se prijavimo kot uporabnik javnost
import auth_public as auth

# Uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # Da šumniki in podobno delujejo pravilno.

import os

with open('secret.txt') as d:
    SECRET = d.read()

# Privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

debug(True) # Pythonova napaka ob sesutju se nam izpiše na spletni strani

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')


@get('/')
def index():
    # preko piškotka ugotovimo, če je uporabnik že prijavljen ali pa ga moramo preusmeriti na prijavo
    user = request.get_cookie('user', secret=SECRET)
    print(user)
    if user is not None:
        p_ali_z, emso = user
        return template('index.tpl', message=None)
    redirect('/login/')


@get('/login/')
def login_get():
    return template('login.tpl', napaka=None, username=None)


@post('/login/')
def login_post():
    username = request.forms.username
    password = request.forms.password # !!! MOGOCE JE TREBA SE HASH
    p = cur.execute('SELECT emso FROM uporabnik_pacient WHERE uporabnisko_ime=%s AND geslo=%s',(username, password))
    if p is None:
        # ni pacienta s tako kombinacijo uporabniskega imena in gesla
        cur.execute('SELECT emso FROM uporabnik_zdravnik WHERE uporabnisko_ime=%s AND geslo=%s',(username, password))
        z = cur.fetchone()
        if z is None:
            # ni niti zdravnika s tako kombinacijo uporabniskega imena in gesla
            return template('login.tpl', napaka='Nepravilna prijava', username=username)
        else:
            # je zdravnik s tako kombinacijo uporabniskega imena in gesla
            response.set_cookie('user', ('z', z), path='/', secret=SECRET)
            redirect('/')
    else:
        # je pacient s tako kombinacijo uporabniskega imena in gesla
        response.set_cookie('user', ('p', p), path='/', secret=SECRET)
        redirect('/')


@get('/zdravniki')
def zdravniki():
    cur.execute('SELECT * FROM zdravnik')
    return template('zdravniki.tpl', zdravniki=cur)


@get('/pacienti')
def pacienti():
    cur.execute("""
    SELECT * FROM pacient
    LEFT JOIN zdravnik ON pacient.zdravnik_emso = zdravnik.emso
    ORDER BY pacient.priimek, pacient.ime
    """)
    return template('pacienti.tpl', pacienti=cur)


@get('/zdravstveni_domovi/<treshold:int>')
def zdravstveni_domovi(treshold):
    cur.execute('SELECT * FROM zdravstveni_dom WHERE kapaciteta >= %s ORDER BY kapaciteta, id', [treshold])
    return template('zdravstveni_domovi.tpl', zdravstveni_domovi=cur, treshold=treshold)


@get('/zaposlitve_zdravnikov')
def zaposlitve_zdravnikov():
    cur.execute("""
    SELECT * FROM zdravnik
    LEFT JOIN zaposlitev ON emso = zaposlitev.zdravnik_emso
    LEFT JOIN zdravstveni_dom ON zdravstveni_dom_id = zdravstveni_dom.id
    """)
    return template('zaposlitve_zdravnikov.tpl', zaposlitve_zdravnikov=cur)


@get('/moj_profil/')
def moj_profil():  
    user = request.get_cookie('user', secret=SECRET)
    p_ali_z, emso = user
    if p_ali_z == 'z':
        cur.execute("""
        SELECT * FROM zdravnik
        LEFT JOIN zaposlitev ON emso = zaposlitev.zdravnik_emso
        LEFT JOIN zdravstveni_dom ON zdravstveni_dom_id = zdravstveni_dom.id
        WHERE emso=%s
        """, [emso[0]])
        zdravnik=cur.fetchone()
        cur.execute("""
        SELECT * FROM pacient 
        WHERE zdravnik_emso=%s
        """,[emso[0]])
        return template('profil_zdravnik.tpl', zdravnik=zdravnik, pacienti=cur)
    else:
        return template('profil_pacient.tpl', pacient=cur)


@get('/dodaj_pacienta')
def dodaj_pacienta():
    return template('dodaj_pacienta.tpl', ime='', priimek='', emso='', st_zdr_zav='', spol='', datum_rojstva='', visina='', teza='', zdravnik_emso='', napaka=None)


@post('/dodaj_pacienta')
def dodaj_pacienta_post():
    ime = request.forms.getunicode('ime')
    priimek = request.forms.getunicode('priimek')
    emso = request.forms.getunicode('emso')
    st_zdr_zav = request.forms.getunicode('st_zdr_zav')
    spol = request.forms.getunicode('spol')
    datum_rojstva = request.forms.getunicode('datum_rojstva')
    visina = request.forms.getunicode('visina')
    teza = request.forms.getunicode('teza')
    zdravnik_emso = request.forms.getunicode('zdravnik_emso')
    try:
        cur.execute('INSERT INTO pacient (emso,zdravstvena_st,ime,priimek,spol,datum_rojstva,teza,visina,zdravnik_emso) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (emso, st_zdr_zav, ime, priimek, spol, datum_rojstva, teza, visina, zdravnik_emso))
    except Exception as e:
        conn.rollback()
        return template('dodaj_pacienta.tpl', ime=ime, priimek=priimek, emso=emso, st_zdr_zav=st_zdr_zav, spol=spol, datum_rojstva=datum_rojstva, visina=visina, teza=teza, zdravnik_emso=zdravnik_emso, napaka='Napaka: %s' % e)
    redirect(url('index'))

###########################################################################################
###########################################################################################
###########################################################################################

# Glavni program

# Priklop na bazo
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
# conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # Onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == '__main__':
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)
