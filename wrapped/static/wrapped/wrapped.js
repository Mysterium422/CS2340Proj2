const sliderWrapper = document.querySelector('.slider-wrapper');
const slides = document.querySelectorAll('.slide');
const leftArrow = document.querySelector('.left-arrow');
const rightArrow = document.querySelector('.right-arrow');

let currentSlide = 0;

function updateSlide(index) {
    sliderWrapper.style.transform = `translateX(-${index * 100}vw)`;
}

leftArrow.addEventListener('click', () => {
    if (currentSlide > 0) {
        currentSlide--;
        updateSlide(currentSlide);
    }
});

rightArrow.addEventListener('click', () => {
    if (currentSlide < slides.length - 1) {
        currentSlide++;
        updateSlide(currentSlide);
    }
});

// Mobile touch support
let touchStartX = 0;

document.addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].clientX;
});

document.addEventListener('touchend', (e) => {
    const touchEndX = e.changedTouches[0].clientX;
    if (touchEndX < touchStartX - 50 && currentSlide < slides.length - 1) {
        // Swipe left
        currentSlide++;
        updateSlide(currentSlide);
    } else if (touchEndX > touchStartX + 50 && currentSlide > 0) {
        // Swipe right
        currentSlide--;
        updateSlide(currentSlide);
    }
});
