// Add item to cart
    $('.plus-cart').click(function() {
        var id = $(this).attr("pid").toString();
        var element = this.parentNode.children[2];
        $.ajax({
            type: "GET",
            url: '/pluscart',
            data: { prod_id: id

             },
            success: function(data) {
                element.innerText = data.quantity
                document.getElementById("amount").innerText = data.amount
                document.getElementById("totalamount").innerText = data.totalamount
            },
        })
        
    });

    // Subtract item from cart
    $('.minus-cart').click(function() {
        var id = $(this).attr("pid").toString();
        var element = this.parentNode.children[2];
        $.ajax({
            type: "GET",
            url: '/minuscart',
            data: { prod_id: id

             },
            success: function(data) {
                element.innerText = data.quantity
                document.getElementById("amount").innerText = data.amount
                document.getElementById("totalamount").innerText = data.totalamount
            },
        })
    });

    // Remove item from cart
    $('.remove-cart').click(function() {
        var id = $(this).attr("pid").toString();
        var element = this
        $.ajax({
            type: "GET",
            url: "/removecart",
            data: { prod_id: id },
            success: function(data) {
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
                eml.parentNode.parentNode.parentNode.parentNode.remove();
            },
            error: function(error) {
                console.log('Error:', error);
            }
        })
    });

