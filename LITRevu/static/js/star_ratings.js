document.addEventListener("DOMContentLoaded", function() {
    const stars = document.querySelectorAll(".star");
    const ratingInput = document.getElementById('ratingInput');

    stars.forEach(function(star) {
        star.addEventListener("mouseover", function() {
            const rating = parseInt(star.getAttribute("data-rating"));
            selectStars(rating);
        });
    });

    function selectStars(rating) {
        ratingInput.value = rating;
        stars.forEach(function(star) {
            const starRating = parseInt(star.getAttribute("data-rating"));
            star.style.color = (starRating <= rating) ? "yellow" : "black";
        });
    }
});
