% rebase('base.tpl', naslov='Zaposlitve zdravnikov')

<p>
  <a href="{{url('/')}}">
    Domov
  </a>
</p>

<table cellpadding="5" cellspacing="0" border="6">
  <tr>
    <th>Ime</th>
    <th>Priimek</th>
    <th>Emšo</th>
    <th>Datum rojstva</th>
    <th>Zdravstveni dom</th>
    <th>Naslov</th>
    <th>Datum zaposlitve</th>
  </tr>
  % for (emso, ime, priimek, _, datum_rojstva, _, _, _, datum_zaposlitve, _, naslov_doma, ime_doma, _) in zaposlitve_zdravnikov:
  <tr>
    <td>{{ime}}</td>
    <td>{{priimek}}</td>
    <td>{{emso}}</td>
    <td>{{datum_rojstva}}</td>
    <td>{{ime_doma}}</td>
    <td>{{naslov_doma}}</td>
    <td>{{datum_zaposlitve}}</td>
  </tr>
  % end
</table>