const sliderWrapper = document.querySelector('.slider-wrapper');
const slides = document.querySelectorAll('.slide');
const leftArrow = document.querySelector('.left-arrow');
const rightArrow = document.querySelector('.right-arrow');

sliderWrapper.style.width = `${slides.length * 100}vw`;

let currentSlide = 0;

function updateSlide(index) {
    sliderWrapper.style.transform = `translateX(-${index * 100}vw)`;
    applyPopInAnimation(index);
    toggleArrows(index);
}

function toggleArrows(index) {
    // Hide left arrow if on the first slide
    if (index === 0) {
        leftArrow.style.display = 'none';
    } else {
        leftArrow.style.display = 'block';
    }

    // Hide right arrow if on the last slide
    if (index === slides.length - 1) {
        rightArrow.style.display = 'none';
    } else {
        rightArrow.style.display = 'block';
    }
}

// Initialize the first slide
toggleArrows(currentSlide);

function applyPopInAnimation(index) {
    // Remove the animation class from all slides
    slides.forEach(slide => {
        slide.querySelectorAll('*').forEach(el => el.classList.remove('pop-in'));
    });

    // Add the animation class to elements of the current slide
    const currentElements = slides[index].querySelectorAll('*');
    currentElements.forEach(el => el.classList.add('pop-in'));
}

// Add event listeners for navigation
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

let keysPressed = [0, 0]

document.addEventListener('keydown', (event) => {
    if (event.key == "ArrowLeft") {
        leftArrow.click()
    } else if (event.key == "ArrowRight") {
        rightArrow.click()
    }
})

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

// Apply pop-in to the initial slide
applyPopInAnimation(currentSlide);
