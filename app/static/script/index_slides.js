/**
 * The original idea of displaying this picture slide is learned from the Internet (from bilibili)
 */
// a list of those 5 dots at the bottom of the picture
let dot = document.querySelectorAll(".dot")
// the whole picture list
let picContainer = document.querySelector(".pic-container")

/*
    The index of the picture that is being shown in the slide panel.
    Range from 0 to picNum-1
 */
let index = 0

// this is for calculating the time interval
let time

/**
 * This method is used to update the position of the picture list horizontally
 * by changing the attribute 'left' of '.pic-container' class in css file.
 */
function refreshPosition() {
    // drag the picture list to left by 'index' times of the picture width
    // (this is because, in the css file we have defined the width of each picture as 100%)
    picContainer.style.left = (index * -100) + "%"
}

/**
 * This method is used to update the current index
 * to the index of the "NEXT picture".
 * (Notice that we will play the pictures circularly)
 */
function goNext() {
    // if the current index has already reached the last picture, we will set it back to the first picture
    if (index >= dot.length-1) {
        index = 0
    } else {
        index++
    }
}

/**
 * This method is used to update the current index
 * to the index of the "LAST picture".
 * (Notice that we will play the pictures circularly)
 */
function goLast() {
    // if the current index has already reached the first picture, we will set it back to the last (final) one.
    if (index < 1) {
        index = dot.length-1
    } else {
        index--
    }
}

/**
 * increase the index by 1 every 5 seconds, which means go into next picture.
 */
function timer(){
    time = setInterval(() => {
        // we will go to the next picture every 5 seconds.
        // goNext() method can check whether should we go back to the first one.
        goNext()
        refreshPosition()
    }, 5000)
}

/**
 * loop through the dot group, add click listener for
 * each dot to go to the correspond picture
 */
for (let i = 0; i < dot.length; i++) {
    dot[i].addEventListener("click", () => {
        index = i
        refreshPosition()
        // we should stop the timer and restart it again,
        // because if not, when we click on a dot button and go to the another picture,
        // the timer has been keeping going, therefore, the time for this new picture can less than the time we have set.
        clearInterval(time)
        timer()
    })
}

// start the timer
timer()