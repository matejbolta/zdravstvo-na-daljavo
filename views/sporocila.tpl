% ime, priimek, emso = pacient

% if p_ali_z == 'z':
%    naslov = f'Sporočila osebe {ime} {priimek}'
% else: 
%    naslov = 'Moja sporočila'
% end
% rebase('base.tpl', naslov=naslov, domov=True, odjava=True)

% if int(sporocila.rowcount) == 0:
Od te osebe še nimate sporočil.

% else:
<table cellpadding="10" cellspacing="0" border="12">
  <tr>
    <th>Datum</th>
    <th>Tema</th>
    <th>Vsebina</th>
    <th>Nujnost</th>
  </tr>
  % for (datum, nujnost, tema, vsebina) in sporocila:
  <tr>
    <td>{{datum}}</td>
    <td>{{tema}}</td>
    <td>{{vsebina}}</td>
    <td>{{nujnost}}</td>
  </tr>
  % end
</table>
% end

% if p_ali_z == 'p':
<h2>Napiši sporočilo</h2>
<button>
<form action="{{url('sporocila', pacient_emso=emso)}}" method="POST">
  <p>Tema   : <input type="text" name="tema" value="{{vnesena_tema}}"></p>
  <p>Vsebina  : <input type="text" name="vsebina" value="{{vnesena_vsebina}}"></p>
  <p>Nujnost  : 
    <select name="nujnost" id="lang", value="{{vnesena_nujnost}}">
      <option value="redno">Redno</option>
      <option value="hitro">Hitro</option>
      <option value="zelo hitro">Zelo hitro</option>
      <option value="nujno">Nujno</option>
      <option value="zelo nujno">Zelo nujno</option>
    </select>
  </p>
  <p><input type="submit" value="Dodaj izvid"></p>
</form>
</button>
% end

<br>
<br>