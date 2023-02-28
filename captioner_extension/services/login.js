export function login(email, password) {
    let data = {
        "email": email,
        "password": password
    }

    return fetch("http://localhost:5000/login", {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
    }).then((res) => {
       return res.json()
    }).then((data) => {
        return data
    }).catch(() => {
        alert("Algo deu errado ao tentar se conectar ao servidor. Tente novamente mais tarde.")
    }) 
}