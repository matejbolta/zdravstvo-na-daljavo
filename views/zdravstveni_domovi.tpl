% rebase('base.tpl', naslov='Zdravstveni domovi s kapaciteto vsaj {} oseb'.format(treshold))

<p>
  <button>
    <a href="{{url('/')}}">
      Domov
    </a>
  </button>
</p>

<table cellpadding="10" cellspacing="0" border="12">
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