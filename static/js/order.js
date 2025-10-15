
document.addEventListener("DOMContentLoaded", () => {
    
    /*console.log("We made it to js");*/

    let product = document.getElementById("product");
    let quantity = document.getElementById("quantity");
    let total = document.getElementById("total_cost");
    let update = document.getElementById("updateCost");

    


    function change(){


        let p = product.value;
        let q = parseFloat(quantity.value);
        
        /* Just scan the product and multiply with some nice formatting
            UPDATE: I needed to add a separate input field for update.
            total is just what displays to the user.        
        */
        if (p === "p1"){
            total.textContent = `Your total is: $${18.00*q}`;
            update.value = 18.00*q;
        }
        else if (p === "p2"){
            total.textContent = `Your total is: $${14.00*q}`;
            update.value = 14.00*q;
        }
        else if (p === "p3"){
            total.textContent = `Your total is: $${13.00*q}`;
            update.value = 13.00*q;
        }
        else if (p === "p4"){
            total.textContent = `Your total is: $${13.00*q}`;
            update.value = 13.00*q;
        }
    }

        

    product.addEventListener("change",change);
    quantity.addEventListener("input",change);


});
