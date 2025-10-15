
/* Adapted from the in class slides */
document.addEventListener("DOMContentLoaded", ()=>{

    let countdown_input = document.getElementById("countdown");
    let state = "on";
    let timer = null;

    let count = 60;
    countdown_input.textContent = `Time until shipment: ${count}`;

    timer = setInterval(()=>{

        countdown_input.textContent = `Time until shipment: ${count}`;
        count-=1;

        if (count < 0){

            count = 0

            clearInterval(timer)

        }
        
    }, 1000);
});
