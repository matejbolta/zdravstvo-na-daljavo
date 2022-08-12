% ime, priimek, emso = pacient

% if p_ali_z == 'z':
%    naslov = f'Izvidi osebe {ime} {priimek}' 
% else: 
%    naslov = 'Moji izvidi'
% end
% rebase('base.tpl', naslov=naslov, domov=True, odjava=True)

% if int(izvidi.rowcount) == 0:
Ta oseba še nima izvidov.

% else:
<table cellpadding="10" cellspacing="0" border="12">
  <tr>
    <th>Datum</th>
    <th>Zdravstveni dom</th>
    <th>Razlog</th>
    <th>Izvid</th>
  </tr>
  % for (datum, razlog, izvid, zdr_dom) in izvidi:
  <tr>
    <td>{{datum}}</td>
    <td>{{zdr_dom}}</td>
    <td>{{razlog}}</td>
    <td>{{izvid}}</td>
  </tr>
  % end
</table>
% end

% if napaka:
  <p class="warning">
    {{napaka}}
  </p>
% end

% if p_ali_z == 'z':
<h2>Dodaj izvid</h2>
<button>
<form action="{{url('izvidi', pacient_emso=emso)}}" method="POST">
  <p>Razlog   : <input type="text" name="razlog" value="{{vnesen_razlog}}"></p>
  <p>Izvid   : <input type="text" name="izvid" value="{{vnesen_izvid}}"></p>
  <p><input type="submit" value="Dodaj izvid"></p>
</form>
</button>
% end

<br>
<br>