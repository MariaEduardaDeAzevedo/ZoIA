export function login(email, password, host) {
    let data = {
        "email": email,
        "password": password,
        "remember": true
    }

    chrome.storage.sync.set({"zoia-host": host})

    return fetch(`${host}/api/login`, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
    }).then((res) => {
        return [res.json(), res.status]
    }).then((data) => {
        //chrome.storage.sync.set({"zoia-token": data.data.token})
        return data
    }).catch(() => {
        alert("Algo deu errado ao tentar se conectar ao servidor. Tente novamente mais tarde.")
    }) 
}