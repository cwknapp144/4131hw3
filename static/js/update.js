
/* Adapted from the in class slides */
document.addEventListener("DOMContentLoaded", ()=>{
    let countdown_input = document.getElementById("countdown");
    let state = "on";
    let timer = null;

    let count = 60;
    countdown_input.textContent = `Time until shipment: ${count}`;

    timer = setInterval(()=>{

        count-=1;

        if (count < 0){

            count = 0

            /* Change the orders.get('status') to shipped */

            clearInterval(timer)

        }
        
        
    }, 1000);
});
