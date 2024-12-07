let timeoutId;

function typeHeadingEffect(element, text, speed, childDiv) {
    let index = 0;
    element.textContent = ''; // Clear existing content
    function type() {
        if (index < text.length) {
            element.textContent += text.charAt(index);
            index++;
            timeoutId = setTimeout(type, speed);
            adjustParentHeight(childDiv);
        } else {
            element.style.borderRight = 'none'; // Hide cursor after typing
        }
    }
    type();
}

function adjustParentHeight(childDiv){
    const parentDiv = document.getElementById("card");
    const childHeight = childDiv.scrollHeight;
    parentDiv.style.height = `${childHeight}px`;

}

let headingSignup = 'Welcome to the Blog Site'
let headingLogin = 'Welcome back to the Blog Site'

document.addEventListener('DOMContentLoaded', () => {

    const url = window.location.href;

    let value ; 

    const cardBack = document.getElementById('card-back');
    const cardFront = document.getElementById('card-front');

    const headingLoginId = document.getElementById('heading-l');
    const headingSignupId = document.getElementById('heading-s');

    if(url.includes('signup')){

        value = true;

        adjustParentHeight(cardFront);

        typeHeadingEffect(headingSignupId,headingSignup,100,cardFront);

        cardBack.style.transform = 'rotateY(180deg)';

    }else{

        value = false;

        adjustParentHeight(cardBack);

        typeHeadingEffect(headingLoginId,headingLogin,100,cardBack);

        cardFront.style.transform = 'rotateY(180deg)';

    }

    const card = document.querySelector('.card');
    const flipButton = document.getElementById('signup-flip-button');
    const flipButtonBack = document.getElementById('login-flip-button');

    flipButton.addEventListener('click', () => {
        typeHeadingEffect(headingLoginId,headingLogin,100,cardBack);
        if(value){
            card.classList.add('flipped');

        }else{
            card.classList.remove('flipped');
        }
        
    });

    flipButtonBack.addEventListener('click', () => {
        typeHeadingEffect(headingSignupId,headingSignup,100,cardFront);
        if(value){
            card.classList.remove('flipped');
        }
        else{
            card.classList.add('flipped');
        }
    });
});
