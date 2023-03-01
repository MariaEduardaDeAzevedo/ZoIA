import { register } from "../services/api.js";

const validationPassword = new RegExp(/(?=^.{8,}$)((?=.*\d)(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$/, "i");
const validationEmail = new RegExp(/^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$/, "i")

let isPassValid = false;
let isEmailValid = false;

var $email = document.getElementById("email");
var $password = document.getElementById("password");
var $passwordConfirmation = document.getElementById("password-confirmation");
var $sendButton = document.getElementById("send-button");

var $passwordInfo = document.getElementById("password-info");
var $passwordInfoModal = document.getElementById("password-info-modal");

var $menuContent = document.getElementById("menu-content");
var $menuPin = document.getElementById("menu-pin");

var emailValue = "";
var $passwordValue = "";

function emailHandle(ev) {
    if (validationEmail.test(ev.target.value)) {
        emailValue = ev.target.value;
        isEmailValid = true;
        $password.removeAttribute("disabled")

        if ($passwordValue != "") {
            $passwordConfirmation.removeAttribute("disabled")
        }

    } else {
        isEmailValid = false;
        $password.setAttribute("disabled", true)
        $passwordConfirmation.setAttribute("disabled", true)
        $sendButton.setAttribute("disabled", true)
        $passwordConfirmation.value = ""
    }
}

$email.addEventListener("keyup", (ev) => {
    emailHandle(ev);
}) 

$email.addEventListener("change", (ev) => {
    emailHandle(ev);
}) 

$password.addEventListener("keyup", (ev) => {
    if (validationPassword.test(ev.target.value)) {
        $passwordValue = ev.target.value;
        $passwordConfirmation.removeAttribute("disabled")
    } else {
        isPassValid = false;
        $passwordValue = "";
        if ($passwordConfirmation.getAttribute("disabled") == null) {
            $passwordConfirmation.setAttribute("disabled", true)
            $passwordConfirmation.value = ""
        }
    }
})  

$passwordConfirmation.addEventListener("keyup", (ev) => {
    if (ev.target.value === $passwordValue) {
        isPassValid = true;
        $sendButton.removeAttribute("disabled")
    } else {
        isPassValid = false;
        $sendButton.setAttribute("disabled", true)
    }
})  

$sendButton.addEventListener("click", (ev) => {
    let data = {
        email: emailValue,
        password: $passwordValue
    }

    register(data)
})

$passwordInfo.addEventListener("mouseover", () => {
    $passwordInfoModal.setAttribute("class", "info-modal")
    console.log("oi")
})

$passwordInfo.addEventListener("mouseout", () => {
    $passwordInfoModal.setAttribute("class", "info-modal hidden")
})

$passwordInfoModal.addEventListener("mouseover", () => {
    $passwordInfoModal.setAttribute("class", "info-modal")
})

$passwordInfoModal.addEventListener("mouseout", () => {
    $passwordInfoModal.setAttribute("class", "info-modal hidden")
})

$menuPin.addEventListener("mouseover", () => {
    $menuContent.style.visibility = "visible"
})

$menuContent.addEventListener("mouseover", () => {
    $menuContent.style.visibility = "visible"
    console.log("in")
})

$menuPin.addEventListener("mouseout", () => {
    $menuContent.style.visibility = "hidden"
})

$menuContent.addEventListener("mouseout", () => {
    $menuContent.style.visibility = "hidden"
})
