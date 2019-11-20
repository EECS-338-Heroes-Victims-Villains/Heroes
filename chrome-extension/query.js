chrome.tabs.query({
    active: true,
    currentWindow: true
}, function (tabs) {
    fetch('http://127.0.0.1:5000/story_chars/?url=' + tabs[0].url).then(data => {
        return data.json()
    }).then(res => {
        console.log(res)
        var h = document.getElementById("hero");
        var vil = document.getElementById("villain");
        var vic = document.getElementById("victim");
        h.appendChild(document.createTextNode(res[0]));
        vil.appendChild(document.createTextNode(res[1]));
        vic.appendChild(document.createTextNode(res[2]));

    })

});

// Open a new connection, using the GET request on the URL endpoint

// request.onload = function () {
//     // Begin accessing JSON data here
// }

// // Send request
// request.send()