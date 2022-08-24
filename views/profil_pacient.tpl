% rebase('base.tpl', naslov='Moj profil', domov=False, odjava=True)

% (emso, zdr_st, ime, priimek, spol, datum_rojstva, teza, visina, _, zdravnik_ime, zdravnik_priimek, _) = podatki

<h3>{{ime}} {{priimek}}</h3>
<p>Emšo: {{emso}}</p>
<p>Št. zdr. zavarovanja: {{zdr_st}}</p>
Datum rojstva: {{datum_rojstva}}
% if spol == 'M':
<p>Spol: Moški</p>
% else:
<p>Spol: Ženski</p>
% end
<p>Višina: {{visina}} cm</p>
<p>Teža: {{teza}} kg</p>
<p>Osebni zdravnik: {{zdravnik_ime}} {{zdravnik_priimek}}</p>

<br>

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