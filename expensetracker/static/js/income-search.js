const searchField = document.getElementById('searchField')
const searchTable = document.querySelector('.search-table')
const mainTable = document.querySelector('.main-table')
const searchResult = document.querySelector('.search-header')
const pagintorContainer = document.querySelector('.paginator-container')
const tableBody = document.getElementById('s-table-body')


searchField.addEventListener('keyup',function(event){
    const searchValue = event.target.value

    if(searchValue.trim().length > 0){
        pagintorContainer.style.display = "none";
        mainTable.style.display = "none";
        tableBody.innerHTML = ''
        fetch('/income/search',{
            body: JSON.stringify({search: searchValue}),
            method: "POST",
            headers: { "X-CSRFToken": getCookie('csrftoken') },
        })
        .then((res) => res.json())
        .then((data) => {
           
            searchTable.style.display = "block";
            mainTable.style.display = "none";
            searchResult.textContent = "Income Info";
         
            if(data.length === 0){
                searchTable.style.display = "none";
                searchResult.textContent = "No Results Found"
            }
            else{
                searchResult.textContent = "Income Info"
                searchTable.style.display="block"
                searchField.autocomplete = data;
                data.map((item) => {
                    tableBody.innerHTML += `
                    <tr>
                        <td>$${item.amount}</td>
                        <td>${item.source_id}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>
                        <td><a href="edit-income/${item.id}" class="btn btn-success">Edit</a></td>
                        <td><a href="delete-income/${item.id}" class="btn btn-danger">Delete</a></td>
                    </tr>
                    `
                })
            }
           

        })
    }
    else{
        searchTable.style.display = "none";
        mainTable.style.display = "block";
        searchResult.textContent = "Income Info"
        pagintorContainer.style.display = "block";
       
      
      
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