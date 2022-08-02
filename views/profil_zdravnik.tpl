% rebase('base.tpl', naslov='Moj profil')

% (emso, ime, priimek, _, datum_rojstva, _, _, _, datum_zaposlitve, _, _, ime_doma, _) = zdravnik

<h2>Moji podatki</h2>
<p>Ime in priimek: {{ime}} {{priimek}}</p>
<p>Datum rojstva: {{datum_rojstva}}</p>
<p>Emšo: {{emso}}</p>
<p>Zaposlitev: {{ime_doma}}</p>
<p>Datum zaposlitve: {{datum_zaposlitve}}</p>

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
      <a href="#link">Sporočila</a>
    </td>
    <td>
      <a href="#link">Izvidi</a>
    </td>
  </tr>
  % end
</table>
