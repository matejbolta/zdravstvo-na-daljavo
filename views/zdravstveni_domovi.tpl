% rebase('base.tpl', naslov='Zdravstveni domovi', domov=True, odjava=True)

% if napaka:
  <p class="warning">
    {{napaka}}
  </p>
% end
<br>
<button>
<form action="{{url('zdravstveni_domovi', treshold=1)}}" method="POST">
  <p>Minimalna kapaciteta  : <input style="text-align:center;" size="1" type="int" name="kapaciteta" value="{{kapaciteta}}"></p>
</form>
</button>
<br><br>
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

<br><br><br><br>