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

    });

    //when clicking on the purchase button
    $("#btn-purchase").on('click', function (){

    });


});


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
                if (thisItem.prev(".btn-cart-dec").hasClass("btn-disabled")) {
                    thisItem.prev(".btn-cart-dec").removeClass("btn-disabled");
                }
            }
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
        }

    });

}