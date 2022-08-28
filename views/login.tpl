% rebase('base.tpl', naslov='Dobrodošli!', domov=False, odjava=False)

<h3>Navodila za prijavo</h3>
<p>
Zdravniki se prijavite z uporabniškim imenom in geslom, ki ste ju dobili v vašem zdravstvenem domu.
</p>
<p>
Drugi uporabniki se prijavite z uporabniškim imenom in geslom, ki ste ju dobili od svojega zdravnika.
<br> Če ste novejši uporabnik, je vaše uporabniško ime sestavljeno iz vašega imena in letnice rojstva (npr. Janez1975), geslo pa je številka vašega zdravstvenega zavarovanja.
</p>

<form class="form-signin" role="form" method="post" action=".">
  <h2 class="form-signin-heading">Prijava</h2>
  
  %if napaka:
  <div class="alert alert-warning">{{napaka}}</div>
  %end
  
  <input type="username" class="form-control" placeholder="Uporabniško ime"
    %if username:
    value="{{username}}"
    %end
    name="username"
    required autofocus>
  
  <input type="password" class="form-control" placeholder="Geslo" name="password" required>
  
  <button class="btn btn-lg btn-primary btn-block" type="submit">Prijava</button>

</form>