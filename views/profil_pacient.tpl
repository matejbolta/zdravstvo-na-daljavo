% rebase('base.tpl', naslov='Moj profil', domov=True, odjava=True)

% (emso, zdr_st, ime, priimek, spol, datum_rojstva, teza, visina, _, zdravnik_ime, zdravnik_priimek, _) = podatki

<h2>Moji podatki</h2>
<p>Ime in priimek: {{ime}} {{priimek}}</p>
<p>Datum rojstva: {{datum_rojstva}}</p>
% if spol == 'M':
<p>Spol: Moški</p>
% else:
<p>Spol: Ženski</p>
% end
<p>Emšo: {{emso}}</p>
<p>Številka zdravstvenega zavarovanja: {{zdr_st}}</p>
<p>Teža: {{teza}} kg</p>
<p>Višina: {{visina}} cm</p>
<p>Osebni zdravnik: {{zdravnik_ime}} {{zdravnik_priimek}}</p>

<p>
<button>
  <a href="{{url('izvidi', pacient_emso=emso)}}">
    Moji izvidi
  </a>
</button>
</p>

<p>
<button>
  <a href="{{url('sporocila', pacient_emso=emso)}}">
    Moja sporočila
  </a>
</button>
</p>

<br>
<br>