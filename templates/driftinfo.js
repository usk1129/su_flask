function validateForm() {
    var rubrik = document.getElementById("rubrik").value;
    var long = document.getElementById("long").value;
    var short = document.getElementById("short").value;
    var username = document.getElementById("username").value;
    var errorarray = new Array();
    var error = false;
    if ( rubrik == "" ) {
        errorarray.push("Titel");
        error = true;
    }
    if ( long == "" ) {
        errorarray.push("Driftinformation för mejl och Wordpress");
        error = true;
    }
    if ( short == "" ) {
        errorarray.push("Driftinformation för Twitter och SMS");
        error = true;
    }
    if ( username == "" ) {
        errorarray.push("Användarnamn");
        error = true;
    }
    if ( error ) {
        alert("Följande fält måste vara ifyllda: " + errorarray.toString());
        return false;
    }
}
