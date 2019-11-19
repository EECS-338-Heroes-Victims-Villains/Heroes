var tabURL = ""

chrome.tabs.query({
    active: true,
    currentWindow: true
}, function (tabs) {
    tabURL = tabs[0].url;
    alert(tabURL);
});
var request = new XMLHttpRequest()

// Open a new connection, using the GET request on the URL endpoint
request.open('GET', 'localhost:5000/story_chars?url=' + tabURL, true)

// request.onload = function () {
//     // Begin accessing JSON data here
// }

// // Send request
// request.send()