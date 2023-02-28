import { login } from "../services/login.js"

chrome.storage.sync.get(["zoia-token"], (obj) => {
    console.log(obj)
})

let email = ""
let password = ""

let $email = document.getElementById("email")
let $password = document.getElementById("password")
let $loginButton = document.getElementById("send-button")


$email.addEventListener("keyup", (ev) => {
    email = ev.target.value
})

$password.addEventListener("keyup", (ev) => {
    password = ev.target.value
})

$loginButton.addEventListener("click", () => {
    login(email, password).then((data) => {
        if (data.status_code === 200) {
            let auth_token = data.data.auth_token
            chrome.storage.sync.set({"zoia-token": auth_token})
            $email.value = ""
            $password.value = ""
            email = ""
            password = ""
            window.location.href = "/index.html"
        } else {
            $email.value = ""
            $password.value = ""
            email = ""
            password = ""
            alert(data.message)
        }
    })
})