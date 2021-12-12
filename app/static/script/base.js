$(document).ready(function (){

    /*
        For changing the theme
    */
    //if the dark theme is clicked, we change the theme
    $("#theme-item-dark").on('click', function () {
        //change theme to dark
        change_theme("dark");
    });

    //if the light theme is clicked, we change the theme
    $("#theme-item-light").on('click', function (){
        //change theme to light
        change_theme("light");
    });

    /*
        For the Admin to delete data in the database
     */
    //if the "delete all" is clicked
    $("#admin-item-delete-all").on('click', function () {
        //delete type should be 'products'
        delete_data("all")
    });


});

//function for changing the theme (use Ajax)
function change_theme(target_theme){
    $.post("/api/change-theme", {
        //send the target theme to server
        "target_theme": target_theme

    }).done(function (response){
        //get from server
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            //we change the theme by switching between different css files
            if (target_theme === 'light'){
                //change the base css file to the "light" one
                $("#css-theme").attr("href", "../static/css/base_style_light.css");

            }else if (target_theme === 'dark'){
                //change the base css file to the "dark" one
                $("#css-theme").attr("href", "../static/css/base_style_dark.css");

            }
        }

    });

}


//function for delete data in database (use Ajax)
function delete_data(type){
    $.post("/api/admin-delete-data", {
        //send the delete type to backend
        "type": type

    }).done(function (response){
       //get from server
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            if (type === "products"){
                window.alert("All the products has been deleted!");

            }else if(type === "all"){
                window.alert("All the data in database has been deleted!");

            }

        }else{
            window.alert("failed to delete data");
        }

    });
}
