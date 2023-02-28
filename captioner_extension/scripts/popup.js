let $switchButton = document.getElementById("switch")
let $switcher = document.getElementById("switcher")
let $status = document.getElementById("activation-status")
let $sessionButton = document.getElementById("session")
let $accountSpan = document.getElementById("account")

let token = false;

chrome.storage.sync.get(["zoia-token"], async (obj) => {
    console.log(obj)
    if (!obj["zoia-token"]) {
        $sessionButton.innerHTML = "Login";
        token = false;
        $accountSpan.innerHTML = ""
    } else {
        $sessionButton.innerHTML = "Logout";
        token = true;
        chrome.storage.sync.get('zoia-token', (obj) => {
            if (obj) {
                let token = obj['zoia-token']
                fetch("http://localhost:5000/account", {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    method: "GET",
                }).then((res) => {
                    return res.json()
                }).then((data) => {
                    if (data.data) {
                        $accountSpan.innerHTML = data.data.email
                    } else {
                        $accountSpan.innerHTML = ""
                    }
                }).catch(() => {
                    alert("Algo deu errado ao tentar se conectar ao servidor. Tente novamente mais tarde.")
                })
            }
        })
    }
})

const openEye = "https://cdn-icons-png.flaticon.com/512/98/98484.png"
const closedEye = "https://cdn-icons-png.flaticon.com/512/98/98488.png"

const browsers = ["Firefox", "Safari", "Chrome", "Opera"];

function enableExtension() {
    $switchButton.setAttribute("enable","")
    $switcher.setAttribute("src", openEye)
    $switcher.setAttribute("alt", "Olho aberto")
    $status.innerHTML = "habilitada"
    
    chrome.storage.sync.set({"zoia-enable": "true"})
}

function disableExtension() {
    $switchButton.removeAttribute("enable")
    $switcher.setAttribute("src", closedEye)
    $switcher.setAttribute("alt", "Olho fechado")
    $status.innerHTML = "desabilitada"

    chrome.storage.sync.set({"zoia-enable":"false"})
}

chrome.storage.sync.get('zoia-enable', (obj) => {
    if ((obj && obj["zoia-enable"] === "true") || !obj) {
        enableExtension();
    } else {
        disableExtension()
    }
})

$switchButton.addEventListener("click", (ev) => {
    if ($switchButton.getAttributeNames().includes("enable")) {
        disableExtension()
    } else {
        enableExtension()
    }
})

$sessionButton.addEventListener("click", () => {
    console.log(token)
    if (!token) {
        console.log("oi")
        window.location.href = "/login.html"
        token = true;
    } else {
        chrome.storage.sync.remove("zoia-token");
        token = false;
        $sessionButton.innerHTML = "Login"
        $accountSpan.innerHTML = ""
    }
})