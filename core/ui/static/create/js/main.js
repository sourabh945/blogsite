let titleInput = document.getElementById("title");
let bodyInput = document.getElementById("body");
let titleCount = document.getElementById("title-count");
let bodyCount = document.getElementById("body-count");

titleInput.addEventListener("input", function() {
    let remainingTitleChars = 126 - titleInput.value.length;
    titleCount.textContent = `${remainingTitleChars} characters left`;
    if (remainingTitleChars < 0) {
        titleCount.style.color = 'red';
    } else {
        titleCount.style.color = '#888';
    }
});

bodyInput.addEventListener("input", function() {
    let remainingBodyChars = 5000 - bodyInput.value.length;
    bodyCount.textContent = `${remainingBodyChars} characters left`;
    if (remainingBodyChars < 0) {
        bodyCount.style.color = 'red';
    } else {
        bodyCount.style.color = '#888';
    }
});

function logoutWarning() {
    if (titleInput.value || bodyInput.value) {
        if (confirm("You have unsaved changes. Do you really want to logout?")) {
            window.location.href = '{% url "logout" %}';
        }
    } else {
        window.location.href = '{% url "logout" %}';
    }
}

function checkForm() {
    if (!titleInput.value || !bodyInput.value) {
        alert("Please fill in both title and blog body.");
    } else {
        alert("Blog successfully created!");
        // Here you would send the data to the server to save it
    }
}

function clearForm() {
    if (titleInput.value || bodyInput.value) {
        if (confirm("Are you sure you want to clear the form?")) {
            titleInput.value = '';
            bodyInput.value = '';
            titleCount.textContent = "126 characters left";
            bodyCount.textContent = "5000 characters left";
        }
    } else {
        titleInput.value = '';
        bodyInput.value = '';
        titleCount.textContent = "126 characters left";
        bodyCount.textContent = "5000 characters left";
    }
}

function homeWarning() {
    if (titleInput.vaule || bodyInput.value) {
        if (confirm('You have unsaved changes. Do you really wanted to go to home page?')){
            window.location.href="{% url 'home' %}";
        }
    } else {
        window.location.href="{% url 'home' %}";
    }
}