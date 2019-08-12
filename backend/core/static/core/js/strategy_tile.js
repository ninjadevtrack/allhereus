
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
    $.fn.strategies_favorites_cud = function (id) {
        var csrfmiddlewaretoken = getCookie('csrftoken');
        var heartNode = $(`#${id}`);
        heartNode.css('pointer-events', 'none');
        if(heartNode.hasClass('heart-active')) {
            $.ajax({
                url: `/strategies/favorites/${id}.json`,
                type: 'DELETE',
                headers: { csrfmiddlewaretoken },
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);
                },
                success: function(data) {
                    if(data.success) {
                        heartNode.removeClass('heart-active').addClass('heart-inactive');
                    }
                    heartNode.attr('alt', "Add to favorites");
                    heartNode.attr('title', "Add to favorites");
                    heartNode.css('pointer-events', 'auto');
                }
            });
        } else if(heartNode.hasClass('heart-inactive')) {
            $.ajax({
                url: `/strategies/favorites/${id}.json`,
                type: 'POST',
                data: {csrfmiddlewaretoken },
                success: function(data) {
                    if(data.success) {
                        heartNode.removeClass('heart-inactive').addClass('heart-active');
                    }
                    heartNode.attr('alt', "Remove from favorites");
                    heartNode.attr('title', "Remove from favorites");
                    heartNode.css('pointer-events', 'auto');
                }
            });
        }
    };
});
