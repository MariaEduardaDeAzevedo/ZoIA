const NOT_ALLOWED_KEYS = ["CapsLock", "Tab"]

let $combinationDisplay = document.getElementById("combination")
let $saveButton = document.getElementById("save-shortcut")

document.addEventListener("keyup", (ev) => {
    console.log(ev.key)
    let content = $combinationDisplay.innerText
    let splittedContent = content.split("+");

    console.log(splittedContent)
    if (ev.key === "Backspace") {
        splittedContent.pop()
    } else if (!NOT_ALLOWED_KEYS.includes(ev.key)) {
        splittedContent.push(ev.key)
    }
    let result = splittedContent.filter(value => value != "");
    $combinationDisplay.innerHTML = result.length > 0 ? result.join(" + ") : "";
})

$saveButton.addEventListener("click", () => {
    console.log($combinationDisplay.innerText.split(" + ").map(value => value.trim()))
})