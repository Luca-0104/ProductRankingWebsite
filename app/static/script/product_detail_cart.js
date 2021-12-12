$(document).ready(function (){

    let btnInc = $("#btn-cart-inc");
    let btnDec = $("#btn-cart-dec");
    let btnAddCart = $("#btn-add-cart");
    let productCountInput = $("#cart-product-count");

    //get the number in the input blank
    let num = parseInt($("#cart-product-count").val());
    //if it is 1, we make the decrease button not clickable
    if (num === 1){
        btnDec.addClass("btn-disabled");

    }else{
        //if the button has this class, we remove it
        if (btnDec.hasClass("btn-disabled")){
            btnDec.removeClass("btn-disabled");
        }
    }

    //when clicking on the add to cart button
    btnAddCart.on("click", function (){add_to_cart(productCountInput.attr("product_id"), productCountInput.val())});

    //when clicking on the increase button
    btnInc.on("click", function (){inc_count()});

    //when clicking on the decrease button
    btnDec.on("click", function (){dec_count()});
});


//add the product into the cart of the current user (using ajax)
function add_to_cart(product_id, product_count){
    $.post("/api/product/add-to-cart", {
        // send to the server (backend)
        "product_id": product_id,
        "product_count": product_count

    }).done(function (response){
        // get from server (backend)
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            window.alert("Add to cart successfully!")
        }

    });
}

//increase the product count
function inc_count(){
    //get the number in the input blank
    let num = parseInt($("#cart-product-count").val());
    //increase the number and set it into the input blank
    $("#cart-product-count").val(num + 1);

    //if value is no longer 1, we make the decrease button clickable again
    if (num + 1 > 1){
        //if the button has this class, we remove it
        if ($("#btn-cart-dec").hasClass("btn-disabled")){
            $("#btn-cart-dec").removeClass("btn-disabled");
        }
    }
}

//decrease the product count
function dec_count(){
    //get the number in the input blank
    let num = parseInt($("#cart-product-count").val());
    //decrease the number and set it into the input blank
    $("#cart-product-count").val(num - 1);

    //if value becomes 1, we make the decrease button not clickable
    if (num - 1 === 1){
        $("#btn-cart-dec").addClass("btn-disabled");
    }
}