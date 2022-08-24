% rebase('base.tpl', naslov='Moj profil', domov=True, odjava=True)

% (emso, ime, priimek, _, datum_rojstva, _, _, _, datum_zaposlitve, _, _, ime_doma, _) = zdravnik

<h3>{{ime}} {{priimek}}</h3>
<p>Emšo: {{emso}}</p>
<p>Datum rojstva: {{datum_rojstva}}</p>
<p>Zaposlitev: {{ime_doma}}</p>
<p>Datum zaposlitve: {{datum_zaposlitve}}</p>
<br>
<h2>Moji pacienti</h2>
<table cellpadding="10" cellspacing="0" border="12">
  <tr>
    <th>Ime</th>
    <th>Priimek</th>
    <th>Emšo</th>
    <th>Št. zdr. zavarovanja</th>
    <th>Spol</th>
    <th>Datum rojstva</th>
    <th>Višina</th>
    <th>Teža</th>
    <th>Sporočila</th>
    <th>Izvidi</th>
  </tr>
  % for (emso, zdravstvena_st, ime, priimek, spol, datum_rojstva, visina, teza, _) in pacienti:
  <tr>
    <td>{{ime}}</td>
    <td>{{priimek}}</td>
    <td>{{emso}}</td>
    <td>{{zdravstvena_st}}</td>
    <td>{{spol}}</td>
    <td>{{datum_rojstva}}</td>
    <td>{{visina}}</td>
    <td>{{teza}}</td>
    <td>
      <a href="{{url('sporocila', pacient_emso=emso)}}">
        Sporočila
      </a>
    </td>
    <td>
      <a href="{{url('izvidi', pacient_emso=emso)}}">
        Izvidi
      </a>
    </td>
  </tr>
  % end
</table>

<p>
  <button>
    <a href="{{url('dodaj_pacienta')}}">
      Dodaj novega pacienta
    </a>
  </button>
</p>

<br>

<h2>Zadnja sporočila</h2>
<table cellpadding="10" cellspacing="0" border="12">
  <tr>
    <th>Pošiljatelj</th>
    <th>Datum</th>
    <th>Tema</th>
    <th>Vsebina</th>
    <th>Nujnost</th>
  </tr>
  % for (ime, priimek, datum, nujnost, tema, vsebina) in sporocila:
  <tr>
    <th>{{ime}} {{priimek}}</th>
    <td>{{datum}}</td>
    <td>{{tema}}</td>
    <td>{{vsebina}}</td>
    <td>{{nujnost}}</td>
  </tr>
  % end
</table>

<br><br><br><br>