const searchField = document.getElementById('searchField')

searchField.addEventListener('keyup',function(event){
    const searchValue = event.target.value

    if(searchValue.trim().length > 0){
        fetch('/expenses/search/',{
            body: JSON.stringify({search: searchValue}),
            method: "POST",
            headers: { "X-CSRFToken": getCookie('csrftoken') },
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data",data)
        })
    }
})

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}