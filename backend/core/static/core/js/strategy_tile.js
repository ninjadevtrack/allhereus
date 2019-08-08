
$(document).ready(function(){
    $.fn.add_strategy_favorites = function (id) {
        $.get(`/strategies/favorites/${id}.json`, function(data, status) {
            if(data.success) {
                if(data.result == 1) {
                    $(`#${id}`).removeClass('heart-inactive').addClass('heart-active');
                } else {
                    $(`#${id}`).removeClass('heart-active').addClass('heart-inactive');
                }

            }
        }) 
    };
});