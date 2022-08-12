% rebase('base.tpl', naslov='Zdravstveni domovi s kapaciteto vsaj {} oseb'.format(treshold), domov=True, odjava=True)

% if napaka:
  <p class="warning">
    {{napaka}}
  </p>
% end

<button>
<form action="{{url('zdravstveni_domovi', treshold=1)}}" method="POST">
  <p>Pokaži domove s kapaciteto, večjo od   : <input type="int" name="kapaciteta" value="{{kapaciteta}}"></p>
</form>
</button>

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

<br>
<br>