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

function getImages(element) {
    let images = []
    searchImages(element, images)

    let srcs = images.map((val, i, array) => {
        return val.getAttribute("src")
    });

    chrome.storage.sync.get("zoia-token", (obj) => {
        if (obj["zoia-token"]) {
            fetch("http://localhost:5000/captioner", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${obj["zoia-token"]}`
                }, 
                body: JSON.stringify({"imgs_src": srcs})
            }).then((res) => {
                return res.json()
            }).then((data) => {
                if (data.data) {
                    captions = data.data.captions
                    for (let index = 0; index < images.length; index++) {
                        const element = images[index];
                        const caption = captions[index]
                        
                        element.setAttribute("alt", caption);
                    }
                }
            }) 
        } else {
            alert("O ZoIA está habilitado, mas não há contas logadas. Faça login para continuar!")
        }
    })
}

window.document.addEventListener("keydown", (ev) => {
    chrome.storage.sync.get("zoia-enable", (obj) => {
        console.log("Shoot!")
        if (!obj || obj["zoia-enable"] === "true") {
            if (ev.shiftKey && ev.key === "Z" && ev.altKey) {
                let element = window.document.activeElement
                console.log(element)
                getImages(element)
            }
        }
    })
})

chrome.storage.sync.get("zoia-enable", (obj) => {
    if (!obj || obj["zoia-enable"] === "true") {
        chrome.storage.sync.set({"zoia-enable": "true"})
    }
})