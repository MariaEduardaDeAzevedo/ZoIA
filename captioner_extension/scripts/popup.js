import { get_account } from "../services/account.js"

let $switchButton = document.getElementById("switch")
let $switcher = document.getElementById("switcher")
let $status = document.getElementById("activation-status")
let $sessionButton = document.getElementById("session")
let $configurationButton = document.getElementById("configurations")
let $accountSpan = document.getElementById("account")

let token = false;

chrome.storage.sync.get(["zoia-token"], (obj) => {
    console.log(obj["zoia-token"])
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
                let account = get_account(token)

                chrome.storage.sync.get('zoia-user', (obj) => {
                    if (obj['zoia-user']) {
                        $accountSpan.innerHTML = obj['zoia-user']
                    } else {
                        $accountSpan.innerHTML = ""
                    }
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
    if (!token) {
        window.location.href = "/login.html"
        token = true;
    } else {
        chrome.storage.sync.remove("zoia-token");
        token = false;
        $sessionButton.innerHTML = "Login"
        $accountSpan.innerHTML = ""
    }
})

$configurationButton.addEventListener("click", () => {
    window.location.href = "/configurations.html"
})

chrome.storage.sync.get("zoia-config-shortcut", (obj) => {
    console.log(obj["zoia-config-shortcut"])
})