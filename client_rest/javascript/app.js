token = localStorage.getItem("accessToken")

owners = document.getElementById('clients')

const getClients = async () => {
    console.log(token)
    var myHeaders = new Headers();
    myHeaders.append("Authorization", `Bearer ${token}`);

    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
    };

    const response = await fetch(
        'http://127.0.0.1:8000/api/clients',
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
            el.innerHTML = `ID: ${client.id}<br>Firstname: ${client.firstname}<br>Last name: ${client.lastname}`
            clients.appendChild(el)
        }
    }
}

getClients()