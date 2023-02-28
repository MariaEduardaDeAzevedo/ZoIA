export const BASE_URL = "http://localhost:5000/"

export function register(data) {
    return fetch(BASE_URL + "user", {
        method: "POST",
        body: JSON.stringify(data)
    }).then((res) => 
        res.json()
    ).then((d) => {
        alert(d.message)
        
        if (d.status_code === 200) {
            window.location.href = "http://localhost:5500/login.html"
        } else {
            window.location.href = window.location.href
        }
    }).catch((e) => {
        console.log(e)
    })
}

export function login(data) {
    fetch(BASE_URL + "login", {
        method: "POST",
        body: JSON.stringify(data)
    }).then((res) => 
        res.json()
    ).then((d) => {
        try {
            chrome.storage.sync.set({"zoia-token": d.data["auth_token"]})
            alert("Login realizado com sucesso!")
            window.location.href = window.location.href
        } catch {
            alert(d.message)
        }
    }).catch((e) => {
        console.log(e)
    })
}