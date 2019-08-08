
$(document).ready(function() {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    $.fn.strategies_favorites_remove = function (id) {
        var csrfmiddlewaretoken = getCookie('csrftoken');
        $.ajax({
            url: `/strategies/favorites/remove/${id}.json`,
            type: 'DELETE',
            headers: { csrfmiddlewaretoken },
            success: function(data) {
                if(data.success) {
                    $(`#${id}`).removeClass('heart-active').addClass('heart-inactive');
                }
            }
        });
    };
    
    $.fn.strategies_favorites_add = function (id) {
        var csrfmiddlewaretoken = getCookie('csrftoken');
        $.ajax({
            url: `/strategies/favorites/add/${id}.json`,
            type: 'POST',
            data: {csrfmiddlewaretoken },
            success: function(data) {
                if(data.success) {
                    $(`#${id}`).removeClass('heart-inactive').addClass('heart-active');
                }
            }
        });
    };
});