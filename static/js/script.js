function showToast(message, type) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${message}</span>`;
    
    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('hide');
        toast.addEventListener('animationend', () => {
            toast.remove();
        });
    }, 3000);
}

$(window).on('load', function() {
    $('body').addClass('loaded');
    if (window.location.pathname.includes('/')) {
        applyAmbilight();
    }
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

    // Modal Close Logic
    $('.modal-close').click(function() {
        $('.modal, .surprise-modal').fadeOut();
        $('#trailerFrame').attr('src', ''); // Stop video
    });

    $(window).click(function(event) {
        if ($(event.target).is('.modal, .surprise-modal')) {
            $('.modal, .surprise-modal').fadeOut();
            $('#trailerFrame').attr('src', ''); // Stop video
        }
    });
});

function openTrailer(url) {
    if (!url) {
        showToast("No trailer available.", "error");
        return;
    }

    let parsedUrl;
    try {
        parsedUrl = new URL(url, window.location.origin);
    } catch (e) {
        showToast("Invalid trailer URL.", "error");
        return;
    }

    const host = parsedUrl.hostname.replace(/^www\./, '');
    const isYoutube = host === 'youtube.com' || host === 'youtu.be';
    if (!isYoutube) {
        showToast("Unsupported trailer source.", "error");
        return;
    }

    // Convert watch/share URL to embed URL.
    if (host === 'youtube.com' && parsedUrl.pathname === '/watch') {
        const videoId = parsedUrl.searchParams.get('v');
        if (!videoId) {
            showToast("Invalid trailer URL.", "error");
            return;
        }
        url = `https://www.youtube.com/embed/${videoId}`;
    } else if (host === 'youtu.be') {
        const videoId = parsedUrl.pathname.replace('/', '');
        if (!videoId) {
            showToast("Invalid trailer URL.", "error");
            return;
        }
        url = `https://www.youtube.com/embed/${videoId}`;
    } else {
        url = parsedUrl.toString();
    }

    $('#trailerFrame').attr('src', `${url}?autoplay=1`);
    $('#trailerModal').fadeIn().css('display', 'flex');
}

/* --- ELITE FEATURE: SURPRISE ME SLOT MACHINE --- */
async function startSurpriseMachine() {
    const modal = document.getElementById('surpriseModal');
    const reel = document.getElementById('slot-reel');
    const title = document.getElementById('surprise-title');
    
    // Show modal
    modal.style.display = 'flex';
    reel.innerHTML = '';
    reel.style.transition = 'none';
    reel.style.transform = 'translateY(0)';
    title.innerText = "Picking your next movie...";

    try {
        const response = await fetch('/random_movie_data/');
        const data = await response.json();
        
        if (data.error) throw new Error(data.error);

        // Build the reel (15 random + winner at the end)
        let reelHtml = '';
        data.reel.forEach(m => {
            reelHtml += `<img src="${m.image}">`;
        });
        // Add winner at the end
        reelHtml += `<img src="${data.winner.image}">`;
        reel.innerHTML = reelHtml;

        // Force reflow
        reel.offsetHeight;

        // Animate
        const itemHeight = 390; // 380px img + 10px gap
        const totalItems = data.reel.length;
        reel.style.transition = 'transform 3s cubic-bezier(0.45, 0.05, 0.55, 0.95)';
        reel.style.transform = `translateY(-${totalItems * itemHeight}px)`;

        // Handle conclusion
        setTimeout(() => {
            title.innerHTML = `Found it: <span style="color: var(--primary-color)">${data.winner.title}</span>`;
            confettiEffect();
            setTimeout(() => {
                window.location.href = data.winner.url;
            }, 2000);
        }, 3200);

    } catch (err) {
        showToast("Add more movies to use this!", "error");
        modal.style.display = 'none';
    }
}

function confettiEffect() {
    // Basic CSS confetti or just skip if no lib
}

/* --- ELITE FEATURE: VOICE SEARCH --- */
function startVoiceSearch() {
    const btn = document.querySelector('.voice-search-btn');
    const input = document.getElementById('main-search');
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        showToast("Voice search not supported in this browser.", "error");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    
    btn.classList.add('listening');
    showToast("Listening...", "info");

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        input.value = transcript;
        btn.classList.remove('listening');
        // Trigger HTMX search
        input.dispatchEvent(new Event('keyup'));
    };

    recognition.onerror = () => {
        btn.classList.remove('listening');
        showToast("Couldn't hear you. Try again.", "error");
    };

    recognition.start();
}

/* --- ELITE FEATURE: AMBILIGHT COLOR MORPHING --- */
function applyAmbilight() {
    const banner = document.querySelector('.trailer_frame iframe, .movie img, .hero-img');
    if (!banner) return;

    // We can't easily read cross-origin images via Canvas due to CORS.
    // Instead, we'll extract colors from the main theme or use a fallback.
    // However, if the images are hosted on the SAME domain (local media), we can use this:
    
    const img = new Image();
    img.crossOrigin = "Anonymous";
    
    // Try to get the image source
    let imgSrc = "";
    const detailImg = document.querySelector('.movie img');
    const heroImg = document.querySelector('.hero-img');
    
    if (detailImg) imgSrc = detailImg.src;
    else if (heroImg) imgSrc = heroImg.src;
    
    if (!imgSrc) return;

    // Use a tiny canvas to get the dominant color
    img.onload = function() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 1;
        canvas.height = 1;
        ctx.drawImage(img, 0, 0, 1, 1);
        const [r, g, b] = ctx.getImageData(0, 0, 1, 1).data;
        
        // Update CSS variables
        document.documentElement.style.setProperty('--primary-color', `rgb(${r}, ${g}, ${b})`);
        document.documentElement.style.setProperty('--primary-glow', `rgba(${r}, ${g}, ${b}, 0.4)`);
    };
    img.src = imgSrc;
}
