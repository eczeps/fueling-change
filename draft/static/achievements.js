$(".reset-button").click(call_reset)

$(".report-button").click(add_achieve);

var clicked = false;

/*
* @param event
* changes the text of the button and adds the user to the list of users 
*/
function add_achieve(event){
    console.log("clicked");
    var AID =  $(this).attr('data-tt'); 
    console.log(AID);
    if (clicked == false){
        $(this).text("reset");
        clicked = true;
        // append_achiever(1, "meeeee", "GARCIA");
        send_completed(AID);
    }else{ //if the oops is clicked then it should send a response to the backend to remove the achievement
         //call the function here for reset
         reset(AID);
        //  clicked = false;
    }
}

function call_reset(event){
    var AID =  $(this).attr('data-tt'); 
    reset(AID);
}

function append_achiever(AID, first, last, username, count){ //should take in a response 
    var rowitem = '<tr data-id = "' + AID + '"> <td class ="first">"' + first + 
                '"</td> <td class ="last">"' + last + '"</td> <td class ="username">' + 
                username + '</td> <td class ="count">' + count + '</td></tr>';
    $("#achievers").append(rowitem);
}

function append_achiever2(resp){ //should take in a response 
    // can't use url_for in js
    var usrURL = "/searched-profile/" + resp.username + "/"
    var rowitem = '<tr data-id = "' + resp.AID + '"> <td class ="first">' + resp.first + 
    '</td> <td class ="last">' + resp.last + 
    '</td> <td class ="username"><a href="' + usrURL + '" >' + 
    resp.username + '</a></td> <td class ="count">' + resp.count + '</td></tr>';
    $("#achievers").append(rowitem);
    $("#completed").text("Congrats! You've completed this achievement!");
    document.getElementById("hideshow").style.display = "block";
    console.log("sucess!");
}

function send_completed(aid){
    $.post(URL, {'aid': aid}, append_achiever2, 'json');
}

function reset(aid){
    $.post(URL2, {'aid': aid}, response, 'json');
}

function response(resp){
    location.reload(true);
}