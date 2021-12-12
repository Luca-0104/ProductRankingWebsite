$(document).ready(function (){

    //get the numbers in the count input blanks
    $(".cart-product-count").each(function (){

        if(parseInt($(this).val()) === 1){
            //disable the decrease button
            if(!$(this).prev().hasClass("btn-disabled")){
                $(this).prev().addClass("btn-disabled");
            }

        }else{
            //if the decrease button is disabled, we make it clickable again
            if($(this).prev().hasClass("btn-disabled")){
                $(this).prev().remove("btn-disabled");
            }
        }

    });

    //calculate and update the total price
    update_total_price();



    /*
    * Click listeners---------------------------------------
    */

    //when clicking on the increase button
    $(".btn-cart-inc").on('click', function (){
        //get the value in the input tag
        let val = parseInt($(this).prev().val());
        // increase the count, pass the current number and the "this" and product id
        inc_count(val, $(this), $(this).prev().attr("product_id"));
    });

    //when clicking on the decrease button
    $(".btn-cart-dec").on('click', function (){
        //get the value in the input tag
        let val = parseInt($(this).next().val());
        // decrease the count, pass the current number and the "this" and product id
        dec_count(val, $(this), $(this).next().attr("product_id"));
    });

    //when clicking on the remove button
    $(".btn-cart-remove").on('click', function (){
        // get the cart_id from html
        let cart_id = $(this).attr("cart_id");
        //remove this cart relation
        remove_cart_relation(cart_id);

    });

    //when clicking on the purchase button
    $("#btn-purchase").on('click', function (){
        //call the purchase method
        purchase();
    });

    //when the checkbox state is changed
    $(".cart-checkbox").on('change', function (){
        //inverse the "is_checked"
        if($(this).attr("is_checked") === "is_checked"){
            $(this).attr("is_checked", "is_not_checked");
            console.log($(this).attr("is_checked"));
        }else{
            $(this).attr("is_checked", "is_checked");
        }

        //update the total price
        update_total_price();
    })


});


function update_total_price(){
    let total_price = 0;

    //loop through all the checkboxes, find which has ben checked
    $(".cart-checkbox").each(function () {
        //select out the boxes with attr "is_checked" == is_checked
        if ($(this).attr("is_checked") === "is_checked") {
            /* add the unit price * count into the total price */

            //get product count of this cart relation
            let cart_id = $(this).attr("cart_id");
            let input_id = "#cart-product-count-" + cart_id;
            let product_count = parseInt($(input_id).val());

            //get the product unit price
            let price_id = "#product-price-" + cart_id;
            let unit_price = parseFloat($(price_id).attr("price"));

            //add to the total price
            total_price += (product_count * unit_price);
        }
    });

    //update the span of total price
    $("#total-price").text(total_price);
}



/*
    functions that are using AJAX------------------------------------------------------------
*/

//increase the product count, using ajax
function inc_count(num, thisItem, product_id){

    $.post("/api/cart/update-product-count", {
        "new_count": parseInt(num) + 1,
        "product_id": product_id

    }).done(function (response){
        // get from server (backend)
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            //increase the number and set it into the input blank
            thisItem.prev().val(num + 1);

            //if value is no longer 1, we make the decrease button clickable again
            if (num + 1 > 1) {
                //if the decrease button has this class, we remove it
                if (thisItem.prev().prev().hasClass("btn-disabled")) {
                    thisItem.prev().prev().removeClass("btn-disabled");
                }
            }

            //update total price
            update_total_price();
        }

    });

}


//decrease the product count, using ajax
function dec_count(num, thisItem, product_id){

    $.post("/api/cart/update-product-count", {
        "new_count": parseInt(num) - 1,
        "product_id": product_id

    }).done(function (response){
        // get from server (backend)
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            //decrease the number and set it into the input blank
            thisItem.next().val(num - 1);

            //if value becomes 1, we make the decrease button not clickable
            if (num - 1 === 1) {
                thisItem.addClass("btn-disabled");
            }

            //update total price
            update_total_price();
        }

    });

}

//remove a specific cart relation, using ajax
function remove_cart_relation(cart_id){
    $.post("/api/cart/remove-cart-relation", {
        "cart_id": cart_id

    }).done(function (response){
        // get from server (backend)
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            //remove this row in tale
            let remove_id = "#row-" + cart_id;
            $(remove_id).remove();

            //update the total price
            update_total_price()
        }

    });
}


//the function for purchase all the selected products in the cart (user AJAX)
function purchase(){
    //a list to contain the IDs of cart relations that will be purchased
    let cart_id_list = [];

    //loop through all the checkboxes
    $(".cart-checkbox").each(function () {
        //select out the boxes with attr "is_checked" == is_checked
        if ($(this).attr("is_checked") === "is_checked") {
            cart_id_list.push(parseInt($(this).attr("cart_id")));
        }
    });

    //make the list into json
    let JSON_cart_list = {}
    JSON_cart_list.cart_id_list = JSON.stringify(cart_id_list)

    $.post("/api/cart/purchase", {
        //send the JSONed list of cart id to the backend
        "JSON_cart_list": JSON.stringify(cart_id_list)

    }).done(function (response){
        // get from server (backend)
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            //remove all purchased rows in tale
            for (let i = 0; i < cart_id_list.length; i++){
                //remove this row in tale
                let remove_id = "#row-" + cart_id_list[i];
                $(remove_id).remove();
            }

            //update the total price
            update_total_price()
        }

    });
}