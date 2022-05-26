% rebase('base.tpl', naslov='Zdravniki')

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