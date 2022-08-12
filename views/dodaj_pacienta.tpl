% rebase('base.tpl', naslov='Dodaj pacienta', domov=True, odjava=True)

% if napaka:
  <p class="warning">
    {{napaka}}
  </p>
% end

<button>
<form action="{{url('dodaj_pacienta')}}" method="POST">
  <p>Ime   : <input type="text" name="ime" value="{{ime}}"></p>
  <p>Priimek   : <input type="text" name="priimek" value="{{priimek}}"></p>
  <p>Emšo    : <input type="text" name="emso" value="{{emso}}"></p>
  <p>Št. zdr. zavarovanja    : <input type="text" name="st_zdr_zav" value="{{st_zdr_zav}}"></p>
  <p>Spol (M/F)   : <input type="text" name="spol" value="{{spol}}"></p>
  <p>Datum rojstva (YYYY-MM-DD)   : <input type="text" name="datum_rojstva" value="{{datum_rojstva}}"></p>
  <p>Višina   : <input type="text" name="visina" value="{{visina}}"></p>
  <p>Teža   : <input type="text" name="teza" value="{{teza}}"></p>
  <p><input type="submit" value="Dodaj pacienta"></p>
</form>
</button>