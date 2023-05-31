token = localStorage.getItem("accessToken")

owners = document.getElementById('clients')

const getClients = async () => {
    console.log(token)
    if (!token) {
        window.location.href = "index.html"; 
        return;
    }

    var myHeaders = new Headers();
    myHeaders.append("Authorization", `Bearer ${token}`);

    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
    };

    const response = await fetch(
        "http://127.0.0.1:8000/api/clients/birthday/",
        requestOptions,
      )

    if (response.status === 200) {
        result = await response.json()
        console.log(result)
        clients.innerHTML = ""
        for (client of result) {
            //<li class="list-group-item">An item</li>
            el = document.createElement("li")
            el.className = "list-group-item"
            el.innerHTML = `Firstname: ${client.firstname}<br>Last name: ${client.lastname}<br>Day of birthday: ${client.birthday}`
            clients.appendChild(el)
        }
    }
}

getClients()