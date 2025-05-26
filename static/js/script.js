
function myFuction() {
    let text
    if (confirm("Do you want to continue?\nChoose OK/Cancel") === true) {
        text = "You pressed OK!";
    } else {
        text = "You pressed Cancel!";
    }
    document.getElementById("response").innerHTML = text;
}