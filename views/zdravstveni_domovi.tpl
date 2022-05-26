% rebase('base.tpl', naslov='Zdravstveni domovi z kapaciteto vsaj {} oseb'.format(treshold))

<p>
  <a href="{{url('/')}}">
    Domov
  </a>
</p>

<table cellpadding="5" cellspacing="0" border="6">
  <tr>
    <th>ID</th>
    <th>Ime</th>
    <th>Naslov</th>
    <th>Kapaciteta</th>
  </tr>
  % for (id, naslov, ime, kapaciteta) in zdravstveni_domovi:
  % if kapaciteta >= treshold:
  <tr>
    <td>{{id}}</td>
    <td>{{ime}}</td>
    <td>{{naslov}}</td>
    <td>{{kapaciteta}}</td>
  </tr>
  % end
  % end
</table>