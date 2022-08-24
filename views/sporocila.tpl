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
<br><br>

<h3>Novo sporočilo</h3>
<button>
<form action="{{url('sporocila', pacient_emso=emso)}}" method="POST">
  <p>Nujnost  :
    <select name="nujnost" id="lang", value="{{vnesena_nujnost}}">
      <option value="redno">Redno</option>
      <option value="hitro">Hitro</option>
      <option value="zelo hitro">Zelo hitro</option>
      <option value="nujno">Nujno</option>
      <option value="zelo nujno">Zelo nujno</option>
    </select>
  </p>
  <p>Tema   : <br><input type="text" name="tema" value="{{vnesena_tema}}"></p>
  <p>Vsebina  :<br> <textarea rows="8" cols="50" name="vsebina" value="{{vnesena_vsebina}}"></textarea></p>

  <input type="submit" value="Pošlji sporočilo">
</form>
</button>
% end

<br><br><br><br>