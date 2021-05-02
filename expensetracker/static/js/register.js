let usernameField = document.getElementById('username')
let aliasField = document.getElementById('alias')
let invalidUserNameField = document.querySelector('.invalid-username')
let invalidAliasField = document.querySelector('.invalid-alias')
let emailField = document.getElementById('email')
let invalidEmail = document.querySelector('.invalid-email')
let passwordField = document.getElementById('password')
let showPassword = document.querySelector('.show-password')
let submitBtn = document.querySelector('.submit-btn')

usernameField.addEventListener('keyup', function(e){
    usernameVal = e.target.value
    if(usernameVal.length>0){
        fetch('/auth/validate-username',{
            headers : { 
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({user: usernameVal}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            if(data.username_error){
        
                usernameField.classList.add("is-invalid");
                invalidUserNameField.style.display = "block" ;
                invalidUserNameField.innerHTML=`<p class="text-danger">${data.username_error}</p>`
           
            }
            else{
                
                usernameField.classList.remove("is-invalid");
                invalidUserNameField.style.display = "none" ;
            }
        })
    }
    
})

aliasField.addEventListener('keyup', function(e){
    aliasVal = e.target.value
    if(aliasVal.length>0){
        fetch('/auth/validate-alias',{
            headers : { 
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({alias: aliasVal}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            if(data.alias_error){
        
                aliasField.classList.add("is-invalid");
                invalidAliasField.style.display = "block" ;
                invalidAliasField.innerHTML=`<p class="text-danger">${data.alias_error}</p>`
           
            }
            else{
                
                aliasField.classList.remove("is-invalid");
                invalidAliasField.style.display = "none" ;
            }
        })
    }
    
})


emailField.addEventListener('keyup',function(e){
    emailVal = e.target.value
    if(emailVal.length>0){
        fetch('/auth/validate-email',{
            headers : { 
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({email: emailVal}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            if(data.email_error){
               
                emailField.classList.add("is-invalid");
                invalidEmail.style.display = "block" ;
                invalidEmail.innerHTML=`<p class="text-danger">${data.email_error}</p>`
           
            }
            else{
                emailField.classList.remove("is-invalid");
                invalidEmail.style.display = "none" ;
             
            }
        })
    }

})

showPassword.addEventListener('click',function(e){
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    this.classList.toggle('fa-eye-slash');
})

