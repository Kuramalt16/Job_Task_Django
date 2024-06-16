function toggleGif() {
    var img = document.querySelector('.gif-img');
    var initialSrc = '/static/images/Goose.gif';
    var secondarySrc = '/static/images/Honk.gif';

    // Toggle between initial and secondary GIF
    if (img.src.includes('Goose.gif')) {
        img.src = secondarySrc;

        // After the second GIF finishes, revert back to the initial GIF
        img.addEventListener('load', function() {
            setTimeout(function() {
                img.src = initialSrc;
            }, 900); // Duration of second GIF
        }, { once: true }); // Ensures the event listener is triggered only once
    }
}
