$("#achieves").on
    ("click", ".report-button", reroute);

$(".report-button").click(add_achieve);

var clicked = false;

function add_achieve(event){
    console.log("clicked");
    if (clicked == false){
        $(this).text("oops");
        clicked = true;
    }else{
        $(this).text("Yes!");
        clicked = false;
    }
}

/*
* @param event
* changes the text featured div to include the elements
* of the row that was clicked, then shows the div
*/
function reroute(event) {
    var num  = $(this).closest("tr").attr('data-tt');
    console.log(num);
    console.log("hey");
    var URL = "{{url_for('achieveinfo', AID = " + num + ")}}";
    var URL1 = "{{urld_for('index')}}"
    console.log(URL);
    window.location.href = URL;
}