const NOT_ALLOWED_KEYS = ["CapsLock", "Tab"]

let $combinationDisplay = document.getElementById("combination")
let $saveButton = document.getElementById("save-shortcut")

window.addEventListener("load", () => {
    chrome.storage.sync.get("zoia-config-shortcut", (obj) => {
        $combinationDisplay.innerHTML = obj["zoia-config-shortcut"].join(" + ")
    })
})

document.addEventListener("keyup", (ev) => {
    
    let content = $combinationDisplay.innerText
    let splittedContent = content.split("+");

    if (ev.key === "Backspace") {
        splittedContent.pop()
    } else if (!NOT_ALLOWED_KEYS.includes(ev.key)) {
        splittedContent.push(ev.key)
    }
    let result = splittedContent.filter(value => value != "");
    $combinationDisplay.innerHTML = result.length > 0 ? result.join(" + ") : "";
})

$saveButton.addEventListener("click", () => {
    let keys = $combinationDisplay.innerText.split(" + ").map(value => value.trim())
    
    if (keys.includes("Alt") || keys.includes("Control") || keys.includes("Shift")) {
        chrome.storage.sync.set({"zoia-config-shortcut": keys})
    } else {
        alert("Seu atalho deve conter uma das seguintes teclas: Alt, Shift, Control")

        chrome.storage.sync.get("zoia-config-shortcut", (obj) => {
            $combinationDisplay.innerHTML = obj["zoia-config-shortcut"].join(" + ")
        })
    }
})