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

function append_achiever(AID, first, last){ //should take in a response 
    var rowitem = '<tr data-id = "' + AID + '"> <td id ="first">"' + first + 
                '"</td> <td id ="last">"' + last + '"</td> <td id ="count">1</td></tr>';
    $("#achievers").append(rowitem);
}

function append_achiever2(resp){ //should take in a response 
    var rowitem = '<tr data-id = "' + resp.UID + '"> <td id ="first">' + resp.first + 
                '</td> <td id ="last">' + resp.last + '</td> <td id ="count">1</td></tr>'; //implement count!
    $("#achievers").append(rowitem);
    console.log("sucess!");
}

function send_completed(aid){
    $.post(URL, {'aid': aid}, append_achiever2, 'json');
}


