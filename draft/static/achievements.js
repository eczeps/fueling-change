$(".report-button").click(add_achieve);

var clicked = false;

/*
* @param event
* changes the text of the button to oops and adds the user to the list of users 
*/
function add_achieve(event){
    console.log("clicked");
    var AID =  $(this).attr('data-tt'); 
    console.log(AID);
    if (clicked == false){
        $(this).text("oops");
        clicked = true;
        // append_achiever(1, "meeeee", "GARCIA");
        send_completed(AID);
    }//else{ //if the oops is clicked then it should send a response to the backend to remove the achievement
    //     $(this).text("Yes!");
    //     clicked = false;
    // }
}

function append_achiever(AID, first, last, username, count){ //should take in a response 
    var rowitem = '<tr data-id = "' + AID + '"> <td class ="first">"' + first + 
                '"</td> <td class ="last">"' + last + '"</td> <td class ="username">' + 
                username + '</td> <td class ="count">' + count + '</td></tr>';
    $("#achievers").append(rowitem);
}

// TODO: make the hyperlink appear
function append_achiever2(resp){ //should take in a response 
    var rowitem = '<tr data-id = "' + resp.AID + '"> <td class ="first">' + resp.first + 
    '</td> <td class ="last">' + resp.last + '</td> <td class ="username">' + 
    resp.username + '</td> <td class ="count">' + resp.count + '</td></tr>';
    $("#achievers").append(rowitem);
    $("#completed").text("Congrats! You've completed this achievement!");
    console.log("sucess!");
}

function send_completed(aid){
    $.post(URL, {'aid': aid}, append_achiever2, 'json');
}


