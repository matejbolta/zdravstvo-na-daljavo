% rebase('base.tpl', naslov='Zdravniki', domov=True, odjava=True)

<table cellpadding="10" cellspacing="0" border="12">
  <tr>
    <th>Ime</th>
    <th>Priimek</th>
    <th>Emšo</th>
    <th>Datum rojstva</th>
    <th>Specializacija</th>
    <th>Izkušnje</th>
  </tr>
  % for (emso, ime, priimek, _, datum_rojstva, izkusnje) in zdravniki:
  <tr>
    <td>{{ime}}</td>
    <td>{{priimek}}</td>
    <td>{{emso}}</td>
    <td>{{datum_rojstva}}</td>
    <td>Osebni zdravnik</td>
    <td>{{izkusnje}}</td>
  </tr>
  % end
</table>

<br><br><br><br>