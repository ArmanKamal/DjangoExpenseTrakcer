let usernameField = document.getElementById('username')
let invalidUserNameField = document.querySelector('.invalid-username')




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