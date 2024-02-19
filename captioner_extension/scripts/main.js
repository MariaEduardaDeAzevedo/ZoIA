function searchImages(node, list) {
    let nodeChildren = node.children
    if (nodeChildren.length == 0 && node.tagName === "IMG") {
        list.push(node);
    } else if (nodeChildren.length > 0) {
        for (let i = 0; i < nodeChildren.length; i++) {
            const element = nodeChildren[i];
            searchImages(element, list)
        }
    }
}

function getImages(inputElement) {
    let images = []
    searchImages(inputElement, images)

    let srcs = images.map((val, i, array) => {
        return val.getAttribute("src")
    });

    console.log(srcs)

    chrome.storage.sync.get("zoia-token", (obj) => {
        if (obj["zoia-token"]) {
            chrome.storage.sync.get("zoia-host", (o) => {
                if (o["zoia-host"]) {
                    fetch(`${o["zoia-host"]}/api/captioner`, {
                    mode: 'cors',
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json", 
                        "Authorization": `Bearer ${obj["zoia-token"]}`
                    }, 
                    body: JSON.stringify({"images_srcs": srcs})
                }).then((res) => {
                    return res.json()
                }).then((data) => {
                    if (data) {
                        captions = data
                        for (let index = 0; index < images.length; index++) {
                            const element = images[index];
                            const caption = captions[index]
                            
                            element.setAttribute("alt", caption);
                            
                            let child = generateCaptionElement(caption)
                            inputElement.insertBefore(child, inputElement.firstChild)
                        }
                    }
            }) 
                }
            })
        } else {
            alert("O ZoIA está habilitado, mas não há contas logadas. Faça login para continuar!")
        }
    })
}


function generateCaptionElement(caption) {
    let element = document.createElement("div")
    
    element.innerText = caption
    element.style.position = "sticky"
    element.style.backgroundColor = "#0d1117"
    element.style.color = "#ffffff"
    element.style.padding = "0.2rem"
    element.style.zIndex = "100"

    return element
}

function checkShortCut(shortcut, ev) {
    let result = [];

    for (let index = 0; index < shortcut.length; index++) {
        const key = shortcut[index];

        if (key == "Alt" && ev.altKey) {
            result.push(true)
        } else if (key === "Control" && ev.ctrlKey) {
            result.push(true)
        } else if (key === "Shift" && ev.shiftKey) {
            result.push(true)
        } else if (key === ev.key) {
            result.push(true)
        } else {
            result.push(false)
        }
    }

    return !result.includes(false);
}

window.document.addEventListener("keydown", (ev) => {
    chrome.storage.sync.get("zoia-enable", (obj) => {
        if (!obj || obj["zoia-enable"] === "true") {
            console.log("ENABLE")
            chrome.storage.sync.get("zoia-config-shortcut", (obj) => {
                console.log(obj["zoia-config-shortcut"])
                if (checkShortCut(obj["zoia-config-shortcut"], ev)) {
                    let element = window.document.activeElement
                    getImages(element)
                }  
            })
        }
    })
})

chrome.storage.sync.get("zoia-enable", (obj) => {
    if (!obj || obj["zoia-enable"] === "true") {
        chrome.storage.sync.set({"zoia-enable": "true"})
    }
})

chrome.storage.sync.get("zoia-config-shortcut", (obj) => {
    if (!obj || obj["zoia-config-shortcut"] === undefined) {
        chrome.storage.sync.set({"zoia-config-shortcut": ["Z", "Shift", "Alt"]});
    }
})