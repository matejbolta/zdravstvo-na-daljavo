% rebase('base.tpl', naslov='Dodaj pacienta')

<p>
  <button>
    <a href="{{url('/')}}">
      Domov
    </a>
  </button>
</p>

% if napaka:
  <p class="warning">
    {{napaka}}
  </p>
% end

<button>
<form action="{{url('dodaj_pacienta')}}" method="POST">
  <p>Ime   : <input type="text" name="ime" value="{{ime}}"></p>
  <p>Priimek   : <input type="text" name="priimek" value="{{priimek}}"></p>
  <p>Emšo (13-mesten)   : <input type="text" name="emso" value="{{emso}}"></p>
  <p>Št. zdr. zavarovanja (7-mestna)   : <input type="text" name="st_zdr_zav" value="{{st_zdr_zav}}"></p>
  <p>Spol (M/F)   : <input type="text" name="spol" value="{{spol}}"></p>
  <p>Datum rojstva (YYYY-MM-DD)   : <input type="text" name="datum_rojstva" value="{{datum_rojstva}}"></p>
  <p>Višina   : <input type="text" name="visina" value="{{visina}}"></p>
  <p>Teža   : <input type="text" name="teza" value="{{teza}}"></p>
  <p>Emšo zdravnika   : <input type="text" name="zdravnik_emso" value="{{zdravnik_emso}}"></p>
  <p><input type="submit" value="Dodaj pacienta"></p>
</form>
</button>