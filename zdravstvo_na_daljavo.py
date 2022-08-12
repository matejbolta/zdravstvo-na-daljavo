#!/usr/bin/python
# -*- encoding: utf-8 -*-

import time
# Uvozimo bottle. Bottleext nam omogoča pravilno lepljenje URLjev, da ne pride to težav pri pogonu iz oblaka (binder)
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
    if user is not None:
        if user[0] == 'z':
            return template('index.tpl', message=None)
        else:
            redirect(url('/moj_profil/'))
    redirect('/login/')


@get('/login/')
def login_get():
    return template('login.tpl', napaka=None, username=None)

# primer uporabniškega imena in gesla za zdravnika:
#   Allison2397
#   9MrO4aI1
# za pacienta:
#   Philbert4242
#   nb0PxTarICH


@post('/login/')
def login_post():
    username = request.forms.username
    password = request.forms.password # !!! MOGOCE JE TREBA SE HASH
    cur.execute('SELECT emso FROM uporabnik_pacient WHERE uporabnisko_ime=%s AND geslo=%s',(username, password))
    p = cur.fetchone()
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
    return template('zdravstveni_domovi.tpl', zdravstveni_domovi=cur, treshold=treshold, kapaciteta=treshold, napaka=None)


@post('/zdravstveni_domovi/<treshold:int>')
def zdravstveni_domovi(treshold):
    kapaciteta = request.forms.getunicode('kapaciteta')
    try:
        cur.execute('SELECT * FROM zdravstveni_dom WHERE kapaciteta >= %s ORDER BY kapaciteta, id', [kapaciteta])
    except Exception as e:
        conn.rollback()
        cur.execute('SELECT * FROM zdravstveni_dom WHERE kapaciteta >= %s ORDER BY kapaciteta, id', [treshold])
        return template('zdravstveni_domovi.tpl', zdravstveni_domovi=cur, treshold=treshold, kapaciteta=kapaciteta, napaka='Napaka: %s' % e)
    else:
        redirect(url('zdravstveni_domovi', treshold=kapaciteta))


@get('/moj_profil/')
def moj_profil():  
    user = request.get_cookie('user', secret=SECRET)
    p_ali_z, emso = user
    if p_ali_z == 'z':
        cur.execute("""
        SELECT * FROM zdravnik
        LEFT JOIN zaposlitev ON emso = zaposlitev.zdravnik_emso
        LEFT JOIN zdravstveni_dom ON zdravstveni_dom_id = zdravstveni_dom.id WHERE emso=%s
        """, [emso[0]])
        zdravnik = cur.fetchone()
        cur.execute("""
        SELECT ime, priimek, datum, nujnost, tema, vsebina
        FROM (sporocilo JOIN pacient_okrnjen ON sporocilo.pacient_emso = pacient_okrnjen.emso)
        WHERE zdravnik_emso=%s
        ORDER BY datum DESC
        """, [emso[0]])
        sporocila = cur.fetchmany(10)
        cur.execute("SELECT * FROM pacient WHERE zdravnik_emso=%s", [emso[0]])
        return template('profil_zdravnik.tpl', zdravnik=zdravnik, sporocila = sporocila, pacienti=cur)
    else:
        cur.execute("""
        SELECT * FROM pacient 
        JOIN zdravnik_okrnjen ON pacient.zdravnik_emso=zdravnik_okrnjen.zdravnik_emso
        WHERE emso=%s
        """, [emso[0]])
        podatki = cur.fetchone()
        return template('profil_pacient.tpl', podatki=podatki)


@get('/sporocila/<pacient_emso>')
def sporocila(pacient_emso):
    user = request.get_cookie('user', secret=SECRET)
    p_ali_z, _ = user
    cur.execute('SELECT ime, priimek, emso FROM pacient WHERE emso=%s', [pacient_emso])
    pacient = cur.fetchone()
    cur.execute("""
        SELECT datum, nujnost, tema, vsebina FROM sporocilo
        WHERE pacient_emso=%s
        """, [pacient_emso])
    return template('sporocila.tpl', pacient=pacient, sporocila=cur, p_ali_z=p_ali_z, vnesena_tema='', vnesena_vsebina='', vnesena_nujnost='', napaka=None)


@post('/sporocila/<pacient_emso>')
def sporocila(pacient_emso):
    tema = request.forms.getunicode('tema')
    vsebina = request.forms.getunicode('vsebina')
    nujnost = request.forms.getunicode('nujnost')
    datum = time.strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("""
        SELECT pacient.zdravnik_emso FROM pacient 
        JOIN zdravnik_okrnjen ON pacient.zdravnik_emso=zdravnik_okrnjen.zdravnik_emso
        WHERE emso=%s
        """, [pacient_emso])
    zdravnik_emso = cur.fetchone()
    try:
        cur.execute('INSERT INTO sporocilo (pacient_emso, datum, zdravnik_emso, nujnost, tema, vsebina) VALUES (%s, %s, %s, %s, %s, %s)',
                    (pacient_emso, datum, zdravnik_emso[0], nujnost, tema, vsebina))
    except Exception as e:
        conn.rollback()
        user = request.get_cookie('user', secret=SECRET)
        p_ali_z, _ = user
        cur.execute('SELECT ime, priimek, emso FROM pacient WHERE emso=%s', [pacient_emso])
        pacient = cur.fetchone()
        cur.execute("""
            SELECT datum, nujnost, tema, vsebina FROM sporocilo
            WHERE pacient_emso=%s
            """, [pacient_emso])
        return template('sporocila.tpl', pacient=pacient, sporocila=cur, p_ali_z=p_ali_z, vnesena_tema=tema, vnesena_vsebina=vsebina, vnesena_nujnost=nujnost, napaka='Napaka: %s' % e)
    else:
        redirect(url('sporocila', pacient_emso=pacient_emso))


@get('/izvidi/<pacient_emso>')
def izvidi(pacient_emso):
    user = request.get_cookie('user', secret=SECRET)
    p_ali_z, _ = user
    cur.execute('SELECT ime, priimek, emso FROM pacient WHERE emso=%s', [pacient_emso])
    pacient = cur.fetchone()
    cur.execute("""
        SELECT datum, razlog, izvid, ime FROM pregled
        JOIN zdravstveni_dom ON zdravstveni_dom.id = zdravstveni_dom_id
        WHERE pacient_emso=%s
        """, [pacient_emso])
    return template('izvidi.tpl', pacient=pacient, izvidi=cur, p_ali_z=p_ali_z, vnesen_razlog='', vnesen_izvid='', napaka=None)


@post('/izvidi/<pacient_emso>')
def izvidi(pacient_emso):
    razlog = request.forms.getunicode('razlog')
    izvid = request.forms.getunicode('izvid')
    datum = time.strftime('%Y-%m-%d %H:%M:%S')
    user = request.get_cookie('user', secret=SECRET)
    _, zdravnik_emso = user
    cur.execute("""SELECT id FROM zdravstveni_dom 
        JOIN zaposlitev ON zaposlitev.zdravstveni_dom_id=zdravstveni_dom.id
        WHERE zdravnik_emso = %s
        """, [zdravnik_emso[0]])
    zdravstveni_dom_id = cur.fetchone()[0]
    try:
        cur.execute('INSERT INTO pregled (pacient_emso, datum, zdravstveni_dom_id, zdravnik_emso, razlog, izvid) VALUES (%s, %s, %s, %s, %s, %s)',
                    (pacient_emso, datum, zdravstveni_dom_id, zdravnik_emso[0], razlog, izvid))
    except Exception as e:
        conn.rollback()
        user = request.get_cookie('user', secret=SECRET)
        p_ali_z, _ = user
        cur.execute('SELECT ime, priimek, emso FROM pacient WHERE emso=%s', [pacient_emso])
        pacient = cur.fetchone()
        cur.execute("""
        SELECT datum, razlog, izvid, ime FROM pregled
        JOIN zdravstveni_dom ON zdravstveni_dom.id = zdravstveni_dom_id
        WHERE pacient_emso=%s
        """, [pacient_emso])
        return template('izvidi.tpl', pacient=pacient, izvidi=cur, p_ali_z=p_ali_z, vnesen_razlog=razlog, vnesen_izvid=izvid, napaka='Napaka: %s' % e)
    else:
        redirect(url('izvidi', pacient_emso=pacient_emso))


@get('/dodaj_pacienta')
def dodaj_pacienta():
    return template('dodaj_pacienta.tpl', ime='', priimek='', emso='', st_zdr_zav='', spol='', datum_rojstva='', visina='', teza='', napaka=None)


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
    user = request.get_cookie('user', secret=SECRET)
    _, zdravnik_emso = user
    try:
        cur.execute('INSERT INTO pacient (emso, zdravstvena_st, ime, priimek, spol, datum_rojstva, teza, visina, zdravnik_emso) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (emso, st_zdr_zav, ime, priimek, spol, datum_rojstva, teza, visina, zdravnik_emso[0]))
    except Exception as e:
        conn.rollback()
        return template('dodaj_pacienta.tpl', ime=ime, priimek=priimek, emso=emso, st_zdr_zav=st_zdr_zav, spol=spol, datum_rojstva=datum_rojstva, visina=visina, teza=teza, zdravnik_emso=zdravnik_emso[0], napaka='Napaka: %s' % e)
    redirect(url('index'))

@get("/logout/")
def logout():
    response.delete_cookie('user')
    redirect('/login/')

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
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)
