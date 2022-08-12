% rebase('base.tpl', naslov='Pacienti', domov=True, odjava=True)

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
    <th>Osebni zdravnik</th>
  </tr>
  % for (emso, zdravstvena_st, ime, priimek, spol, datum_rojstva, visina, teza, _, _, zdravnik_ime, zdravnik_priimek, _, _, _) in pacienti:
  <tr>
    <td>{{ime}}</td>
    <td>{{priimek}}</td>
    <td>{{emso}}</td>
    <td>{{zdravstvena_st}}</td>
    <td>{{spol}}</td>
    <td>{{datum_rojstva}}</td>
    <td>{{visina}}</td>
    <td>{{teza}}</td>
    <td>{{zdravnik_ime}} {{zdravnik_priimek}}</td>
  </tr>
  % end
</table>

<br>
<br>