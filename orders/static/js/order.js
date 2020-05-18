// add or remove items in cart page by triggering the plus and minus sign
//
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.minus-btn').forEach(function(button) {
        button.onclick = function() {
            var name = button.dataset.minus;
            var quan = document.getElementById('quan'+name).value;
            var price = document.getElementById('price'+name).innerHTML;
            var total = document.getElementById('total').innerHTML;
            var sub = quan*price;
            console.log("old total : "+total);
            console.log("old subtotal : "+sub);
            if (quan > 1){
                newquan = quan-1;
            } else {
                newquan = 0; 
            }
            var newsub = price*newquan;
            var newsub1 = newsub.toFixed(2);
            var newtotal = total-sub+newsub;
            var newttl = newtotal.toFixed(2);
            console.log("new total : "+newtotal);
            document.getElementById('quan'+name).value = newquan;
            document.getElementById('sub'+name).innerHTML = '$'+ newsub1;
            document.getElementById('total').innerHTML = newttl;
        };
    });
    document.querySelectorAll('.plus-btn').forEach(function(button) {
        button.onclick = function() {
            var name = button.dataset.plus;
            var price = document.getElementById('price'+name).innerHTML;
            var total = document.getElementById('total').innerHTML;
            var quan = document.getElementById('quan'+name).value;
            var newquan = quan;
            var sub = quan * price;
            console.log("old subtotal : "+sub);
            if (newquan < 200){
                newquan++;
            } else {
                newquan = 200; 
            }
            var newsub = price*newquan;
            var newsub1 = newsub.toFixed(2);
            var newtotal = total-sub+newsub;
            var newttl = newtotal.toFixed(2);
            document.getElementById('quan'+name).value = newquan;
            document.getElementById('sub'+name).innerHTML = '$'+ newsub1;
            document.getElementById('total').innerHTML = newttl;
        };
    });
});