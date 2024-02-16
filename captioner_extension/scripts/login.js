import { login } from "../services/login.js"


let host = ""
let email = ""
let password = ""

try {
    chrome.storage.sync.get("zoia-host",  (obj) => {
        $host.value = obj["zoia-host"] ? obj["zoia-host"] : ""
        host = obj["zoia-host"] ? obj["zoia-host"] : ""
    })
} catch {
    console.log("Deu errado")
}

let $host = document.getElementById("host")
let $email = document.getElementById("email")
let $password = document.getElementById("password")
let $loginButton = document.getElementById("send-button")

$email.addEventListener("keyup", (ev) => {
    email = ev.target.value
})

$password.addEventListener("keyup", (ev) => {
    password = ev.target.value
})

$host.addEventListener("keyup", (ev) => {
    host = ev.target.value
})


$loginButton.addEventListener("click", () => {
    login(email, password, host).then((data) => {
        if (data[1] === 200) {
            data[0].then((res) => {
                chrome.storage.sync.set({"zoia-token": res.data.token})
                $email.value = ""
                $password.value = ""
                $host.value = ""
                email = ""
                password = ""
                host = ""
                window.location.href = "/index.html"
            }).catch((res) => {
                $email.value = ""
                $password.value = ""
                $host.value = ""
                email = ""
                password = ""
                host = ""
                alert("Algo deu errado ao tentar fazer login.")
            })
        } else {
            $email.value = ""
            $password.value = ""
            $host.value = ""
            email = ""
            password = ""
            host = ""
            alert(data.message)
        }
    })
})