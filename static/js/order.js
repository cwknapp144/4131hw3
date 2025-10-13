
document.addEventListener("DOMContentLoaded", () => {
    let product = document.getElementById("product");
    let quantity = document.getElementById("quantity");
    let total = document.getElementById("total_cost");

    let p = product.value;
    let q = quantity.value;
    
    if (p === "p1"){
        total.textContent = 18*q;
    }
    if (p === "p2"){
        total.textContent = 14*q;
    }
    if (p === "p3"){
        total.textContent = 13*q;
    }
    if (p === "p4"){
        total.textContent = 13*q;
    }

});
