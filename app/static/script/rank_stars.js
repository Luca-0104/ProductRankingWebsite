/**
 * This way to change the star color when hovering or clicking
 * is learned from Internet blog https://www.cnblogs.com/sxs161028/p/7249880.html
 */

/*
$(function () {
    $(".rank-stars .star").hover(function(){
        $(this).addClass('hovered-star');
        $(this).prevAll().addClass('hovered-star');
    },function(){
        $(this).removeClass('hovered-star');
        $(this).prevAll().removeClass('hovered-star');
    })

    $(".rank-stars .star").click(function () {
        $(this).addClass('clicked-star');
        $(this).prevAll().addClass('clicked-star');
        $(this).nextAll().removeClass('clicked-star');
    })
})
*/

$(document).ready(function (){

    //when hovering on a start, we change the style of it and all the stars before it
    $(".rank-stars .star").hover(function(){
        $(this).addClass('hovered-star');
        $(this).prevAll().addClass('hovered-star');
    },
        //when the pointer out, we reset the style of it and all the stars before it
        function(){
        $(this).removeClass('hovered-star');
        $(this).prevAll().removeClass('hovered-star');
    })

    //loop through all the starts and set onclick on each of them
    let starList = $(".rank-stars .star");
    starList.each(function (){
        $(this).on('click', function (){
            //get the start id and product id
            rate_product($(this).attr("id"), $(".rank-stars").attr("product_id"));
        });
    });



});

//rate the product using Ajax
function rate_product(star_id, product_id){
    $.post("/api/product/stars/rate", {
        // send to the server (backend)
        "star_id": star_id,
        "product_id": product_id

    }).done(function (response){
        // get from server (backend)
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            //update display
            update_star_display(product_id);
        }

    });
}


//This is used to update the display of stars
function update_star_display(product_id){
    $.post("/api/product/stars", {
        // send to the server (backend)
        "product_id": product_id

    }).done(function (response){
        // get from server (backend)
        let returnValue = response['returnValue'];
        let starNum = response["star_num"]; //how many star this user have given

        if (returnValue === 0) { //success
            //update hint text
            $(".rank-hint").each(function (){
                $(this).text("My Feedback");
            })

            //update the stars
            if (starNum === 1){
                $("#star1").addClass("already-star");
            }else if(starNum === 2){
                $("#star1").addClass("already-star");
                $("#star2").addClass("already-star");
            }else if(starNum === 3){
                $("#star1").addClass("already-star");
                $("#star2").addClass("already-star");
                $("#star3").addClass("already-star");
            }else if(starNum === 4){
                $("#star1").addClass("already-star");
                $("#star2").addClass("already-star");
                $("#star3").addClass("already-star");
                $("#star4").addClass("already-star");
            }else if(starNum === 5){
                $("#star1").addClass("already-star");
                $("#star2").addClass("already-star");
                $("#star3").addClass("already-star");
                $("#star4").addClass("already-star");
                $("#star5").addClass("already-star");

            }
        }
    });
}