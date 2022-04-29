'use strict';


let btns = document.querySelectorAll('button');

btns.forEach(function (i) {
    i.addEventListener('click', function(evt) {
      console.log(i);
    //   evt.preventDefault();
      const obj_appt = evt.target.value;
      console.log(obj_appt);
      const u_id = evt.target.id;
      console.log(u_id);

      const queryString = new URLSearchParams({starttime: obj_appt, userid: u_id})
      const url = `/makeappt?${queryString}`;

      fetch(url)
        .then((response) => response.text())
        .then((result) => { console.log(result);
        document.querySelector('#result-text').innerHTML=`<div class = "scheduledinfo">` + "Appointment scheduled for " + result + `</div>`;


    });
  });})




// document.querySelector('#makeappt').addEventListener(onclick, evt => {
//     // evt.preventDefault();
//     const obj_appt = evt.target.value;

//     const queryString = new URLSearchParams({starttime: obj_appt})
//     const url = `/makeappt?${queryString}`;
    
    
//     //     fetch(url)
//     //         .then((response) => response.text())
//     //         .then((result) => { console.log(result);
//     //         document.querySelector('#result-text').innerHTML=result;
//     //     })
//     // }