$(".addstar-button").click(addStar);

$(".removestar-button").click(removeStar);

//create a list of the starred achievements 
var clickedStar = [];
var clickedUnstar = [];

function addStar(event){
    console.log("clicked add star");
    //get the AID from whichever line was clicked
    var AID =  $(this).closest("tr").attr('data-tt'); 
    console.log(AID);
    //if the AID is not in the clicked then send to backend and add it to the clicked list 
    if(clickedStar.includes(AID) == false){
        console.log("added Star");
        send_star(AID);
        $(this).text("Remove Star");
        //if the AID is in unstar remove it 
        if(clickedUnstar.includes(AID) == true){
            // var index = clickedUnstar.findIndex(AID);
            var index = findIndex(clickedUnstar, AID);
            clickedUnstar.splice(index); //remove the AID from array
        }
        clickedStar.push(AID);
    }else{
        console.log("removed star");
        send_unstar(AID);
        // var index = clickedStar.findIndex(AID);
        var index = findIndex(clickedStar, AID);
        clickedStar.splice(index); //remove the AID from array
        clickedUnstar.push(AID);
        $(this).text("Add Star");
    }
}

function removeStar(event){
    console.log("clicked add star");
    //get the AID from whichever line was clicked
    var AID =  $(this).closest("tr").attr('data-tt'); 
    console.log(AID);
    //if the AID is not in the clicked then send to backend and add it to the clicked list 
    if(clickedUnstar.includes(AID) == false){
        console.log("removing Star");
        send_unstar(AID);
        $(this).text("Add Star");
        //if the AID is in unstar remove it 
        if(clickedStar.includes(AID) == true){
            // var index = clickedStar.findIndex(AID);
            var index = findIndex(clickedStar, AID);
            clickedStar.splice(index); //remove the AID from array
        }
        clickedUnstar.push(AID);
    }else{
        console.log("removed star");
        send_star(AID);
        // var index = clickedUnstar.findIndex(AID);
        var index = findIndex(clickedUnstar, AID);
        clickedUnstar.splice(index); //remove the AID from array
        clickedStar.push(AID);
        $(this).text("Remove Star");
    }
}

function send_star(aid){
    $.post(URL, {'aid': aid}, changeStar, 'json');
}

function send_unstar(aid){
    $.post(URL2, {'aid': aid}, changeStar, 'json');
}

function changeStar(resp){
    console.log("changed star status!");
}

function findIndex(array, elt){
    for(var i = 0; i < array.length; i++)
        if(array[i]==elt){
            return i;
        }
}