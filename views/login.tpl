% rebase('base.tpl', naslov='Dobrodošli!', domov=False, odjava=False)

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