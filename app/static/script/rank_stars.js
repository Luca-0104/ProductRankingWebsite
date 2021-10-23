/**
 * This way to change the star color when hovering or clicking
 * is learned from Internet blog https://www.cnblogs.com/sxs161028/p/7249880.html
 */


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