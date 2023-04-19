"use strict";
const serverUrl = "http://127.0.0.1:8000";

//route: /images
async function uploadImageToS3() {
    // encode input file as base64 string for upload
    let file = document.getElementById("file").files[0];
    let converter = new Promise(function(resolve, reject) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result.toString().replace(/^data:(.*,)?/, ''));
        reader.onerror = (error) => reject(error);
    });
    let encodedString = await converter;

    // clear file upload input field
    document.getElementById("file").value = "";

    // make server call to upload image and return the server upload promise
    return fetch(serverUrl + "/images", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({filename: file.name, filebytes: encodedString})
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new HttpError(response);
        }
    })
}

// Called below
function showUploadedImage(image) {
    document.getElementById("view").style.display = "block";
    let imageElem = document.getElementById("businesscardimage");
    imageElem.src = image["fileUrl"];
    imageElem.alt = image["fileId"];
    return image;
}

// route: /images/{image_id}/detect-text
function rekogDetectImageText(image) {
    // make server call to translate image and return the server upload promise
    return fetch(serverUrl + "/images/" + image["fileId"] + "/detect-text", {
        method: "GET",
        headers: {
            'Accept': 'application/json', 
            'Content-Type': 'application/json'
        },
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new HttpError(response);
        }
    })
}
// expected: {"name":"Joey K. Smith","phone":"770-391-90","email":"info@whitesandtrovel.com","website":null,"address":"299 Newport Lane - Dunwoody, GA 30338"}
function showRekogTextDetectedFromImage(rekogtext) {
    let detectedTextElem = document.getElementById("detectedtext");
    while (detectedTextElem.firstChild) {detectedTextElem.removeChild(detectedTextElem.firstChild);}
    // TextNodes
    /*
    (rekogtext["name"] != null) ? detectedTextElem.appendChild(document.createTextNode('Name: ' + rekogtext["name"])) : detectedTextElem.appendChild(document.createTextNode('Name: <Not detected>'));
    detectedTextElem.appendChild(document.createElement("br"));
    (rekogtext["phone"] != null) ? detectedTextElem.appendChild(document.createTextNode('Phone: ' + rekogtext["phone"])) : detectedTextElem.appendChild(document.createTextNode('Phone: <Not detected>'));
    detectedTextElem.appendChild(document.createElement("br"));
    (rekogtext["email"] != null) ? detectedTextElem.appendChild(document.createTextNode('E-mail: ' + rekogtext["email"])) : detectedTextElem.appendChild(document.createTextNode('E-mail: <Not detected>'));
    detectedTextElem.appendChild(document.createElement("br"));
    (rekogtext["website"] != null) ? detectedTextElem.appendChild(document.createTextNode('Website: ' + rekogtext["website"])) : detectedTextElem.appendChild(document.createTextNode('Website: <Not detected>'));
    detectedTextElem.appendChild(document.createElement("br"));
    (rekogtext["address"] != null) ? detectedTextElem.appendChild(document.createTextNode('Address: ' + rekogtext["address"])) : detectedTextElem.appendChild(document.createTextNode('Address: <Not detected>'));
    */
    // Create Inputs: Set type, id, className.setAttribute value
    detectedTextElem.appendChild(document.createElement("br"));
    var inputname = document.createElement("input"), inputphone = document.createElement("input"), inputemail = document.createElement("input"), inputwebsite = document.createElement("input"), inputaddress = document.createElement("input");
    inputname.type = "text", inputphone.type = "text", inputemail.type = "text", inputwebsite.type = "text", inputaddress.type = "text";
    inputname.id = "inputname", inputphone.id = "inputphone", inputemail.id = "inputemail", inputwebsite.id = "inputwebsite", inputaddress.id = "inputaddress";
    inputname.className = "inputfield", inputphone.className = "inputfield", inputemail.className = "inputfield", inputwebsite.className = "inputfield", inputaddress.className = "inputfield";
    (rekogtext["name"] != null) ? inputname.setAttribute("value", rekogtext["name"]) : inputname.setAttribute("value", "<Not detected>");
    (rekogtext["phone"] != null) ? inputphone.setAttribute("value", rekogtext["phone"]) : inputphone.setAttribute("value", "<Not detected>");
    (rekogtext["email"] != null) ? inputemail.setAttribute("value", rekogtext["email"]) : inputemail.setAttribute("value", "<Not detected>");
    (rekogtext["website"] != null) ? inputwebsite.setAttribute("value", rekogtext["website"]) : inputwebsite.setAttribute("value", "<Not detected>");
    (rekogtext["address"] != null) ? inputaddress.setAttribute("value", rekogtext["address"]) : inputaddress.setAttribute("value", "<Not detected>");
    var labelname = document.createElement("label"), labelphone = document.createElement("label"), labelemail = document.createElement("label"), labelwebsite = document.createElement("label"), labeladdress = document.createElement("label");
    labelname.setAttribute("value", "Name: ");
    labelphone.setAttribute("value", "Phone: ");
    labelemail.setAttribute("value", "E-mail: ");
    labelwebsite.setAttribute("value", "Website: ");
    labeladdress.setAttribute("value", "Address: ");
    labelname.setAttribute("for", "inputname");
    labelphone.setAttribute("for", "inputphone");
    labelemail.setAttribute("for", "inputemail");
    labelwebsite.setAttribute("for", "inputwebsite");
    labeladdress.setAttribute("for", "inputaddress");
    detectedTextElem.appendChild(document.createElement("br"));
    detectedTextElem.appendChild(labelname);
    detectedTextElem.appendChild(document.createElement("br"));
    detectedTextElem.appendChild(inputname);
    detectedTextElem.appendChild(document.createElement("br"));
    detectedTextElem.appendChild(labelphone);
    detectedTextElem.appendChild(document.createElement("br"));
    detectedTextElem.appendChild(inputphone);
    detectedTextElem.appendChild(document.createElement("br"));
    detectedTextElem.appendChild(labelemail);
    detectedTextElem.appendChild(document.createElement("br"));
    detectedTextElem.appendChild(inputemail);
    detectedTextElem.appendChild(document.createElement("br"));
    detectedTextElem.appendChild(labelwebsite);
    detectedTextElem.appendChild(document.createElement("br"));
    detectedTextElem.appendChild(inputwebsite);
    detectedTextElem.appendChild(document.createElement("br"));
    detectedTextElem.appendChild(labeladdress);
    detectedTextElem.appendChild(document.createElement("br"));
    detectedTextElem.appendChild(inputaddress);
}
function uploadImageDetectTextAndDetectEntities() {
    uploadImageToS3()
        .then(image => showUploadedImage(image))
        .then(image => rekogDetectImageText(image))
        .then(rekogtext => showRekogTextDetectedFromImage(rekogtext))
        .catch(error => {
            alert("Frontend Error: " + error);
            console.log("Frontend Error: " + error);
        })
}
class HttpError extends Error {
    constructor(response) {
        super(`${response.status} for ${response.url}`);
        this.name = "HttpError";
        this.response = response;
    }
}
