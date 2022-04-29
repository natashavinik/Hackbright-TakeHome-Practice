'use strict';

let s_dates = (document.getElementByID("alldates")).value

document.getElementById("dadate").addEventListener("change", function(evt){
    if (s_dates.includes(evt.target.value)) {
        console.log ("CANT DO THIS DATE")

    };
})
