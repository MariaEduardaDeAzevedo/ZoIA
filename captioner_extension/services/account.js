export function get_account(token) {
    chrome.storage.sync.get("zoia-host", (obj) => {
        fetch(`${obj["zoia-host"]}/api/account`, {
        headers: {
            'Authorization': `Bearer ${token}`
        },
        method: "GET",
        }).then((res) => {
            return res.json()
        }).then((data) => {
            chrome.storage.sync.set({"zoia-user": data.data.email})
            return data
        }).catch(() => {
            alert("Algo deu errado ao tentar se conectar ao servidor. Tente novamente mais tarde.")
        })
    })
}