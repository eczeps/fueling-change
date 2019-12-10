$("#achieves").on
    ("click", ".report-button", reroute);

$(".report-button").click(add_achieve);

var clicked = false;

/*
* @param event
* changes the text of the button to oops and sends request
*/
function add_achieve(event){
    console.log("clicked");
    if (clicked == false){
        $(this).text("oops");
        clicked = true;
    }else{
        $(this).text("Yes!");
        clicked = false;
    }
    var AID  = $(this).closest("tr").attr('data-tt');
    console.log(AID);
}

/*
* @param event
* changes the text featured div to include the elements
* of the row that was clicked, then shows the div
*/
function reroute(event) {
    var AID  = $(this).closest("tr").attr('data-tt');
    console.log(AID);
    console.log("clicked");
}