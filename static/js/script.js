function showToast(message, type) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${message}</span>`;
    
    container.appendChild(toast);

    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.classList.add('hide');
        toast.addEventListener('animationend', () => {
            toast.remove();
        });
    }, 3000);
}

$(window).on('load', function() {
    $('body').addClass('loaded');
});

$(document).ready(function(){
	$(".toggle img").click(function(){
		$(".menu").slideToggle();
	});

    $(window).scroll(function() {
        if ($(this).scrollTop() > 50) {
            $('.header').addClass('scrolled');
        } else {
            $('.header').removeClass('scrolled');
        }
    });

    // AJAX Favorite Toggle
    $('.fav-btn').click(function() {
        var btn = $(this);
        var movieId = btn.data('id');
        var url = '/'+ movieId + '/favorite/'; // Constructed URL matching urls.py

        $.ajax({
            url: url,
            type: 'GET',
            success: function(response) {
                if (response.status === 'added') {
                    $('#fav-icon').html('♥').css('color', '#c22026');
                    showToast(response.message, 'success');
                } else if (response.status === 'removed') {
                    $('#fav-icon').html('♡').css('color', '#666');
                    showToast(response.message, 'info');
                }
            },
            error: function(xhr) {
                if (xhr.status === 401) {
                    showToast("You must be logged in.", 'error');
                } else {
                    showToast("An error occurred.", 'error');
                }
            }
        });
    });
});