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
    //wishlist
    $('.plus-wishlist').click(function() {
        var id = $(this).attr("pid").toString();
        $.ajax({
            type: "GET",
            url: '/pluswishlist',
            data: { prod_id: id

             },
            success: function(data) {
                //alert(data.message)
                window.location.href = "http://localhost:8000/product_detail/${id}"
            },
        })
        
    });

    $('.minus-wishlist').click(function(){
        var id = $(this).attr("pid").toString();
        $.ajax({
            type: "GET",
            url: '/minuswishlist',
            data: { prod_id: id

             },
            success: function(data) {
                //alert(data.message)
                window.location.href = "http://localhost:8000/product_detail/${id}"
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
        var id=$(this).attr("pid").toString();
        var element=this
        $.ajax({
            type: "GET",
            url: '/removecart',
            data: { 
                prod_id: id 
            },
            success:function(data){
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
                element.parentNode.parentNode.parentNode.parentNode.remove();
            }
        })
    });

    document.getElementById('buyNowButton').addEventListener('click', function(event) {
        // Extract phone number and total amount from form or other sources
        const phoneNumber = document.getElementById('phoneNumberInput').value;
        const totalAmount = parseFloat(document.getElementById('totalAmountInput').value);
    
        // Prepare payload for Mpesa STK Push
        const payload = {
            'phone_number': phoneNumber,
            'amount': totalAmount
        };
    
        // Initiate Mpesa payment using MpesaHandler
        mpesaHandler.make_stk_push(payload);
    
        // Prevent form submission (optional)
        event.preventDefault();
    });
    

