


const reloadButton = document.getElementById('reload-button');
const loadMoreButton = document.getElementById('load-more-button');
const preferenceToggle = document.getElementById('preference-toggle');

const personalizedFeedUrl = document.getElementById('feed-url').value;
const allFeedUrl = document.getElementById('all-feed-url').value;

const nextURL = document.getElementById('next-url');

const blogUrl = window.location.origin + "/blog/";

const feedContainer = document.getElementById('blog-container');

let takeNextUrl = false;

let personalized = true;

function updateTime(startTime) {
    const currentTime = new Date();

    let startTime_ = new Date(startTime);
  
    // Calculate time delta in milliseconds
    const timeDelta = currentTime - startTime_;
  
    // Convert milliseconds to human-readable format
    const totalSeconds = Math.floor(timeDelta / 1000);
    const totalMinutes = Math.floor(totalSeconds / 60);
    const totalHours = Math.floor(totalMinutes / 60);
  
    const hours = totalHours;
    const minutes = totalMinutes % 60;
    const seconds = totalSeconds % 60;
  
    const formattedTime = `${hours} hours, ${minutes} minutes, ${seconds} seconds`;

    return formattedTime
}

async function get_feed() {
    const url = takeNextUrl ? nextURL.value : (personalized ? personalizedFeedUrl : allFeedUrl);
    return await fetch(url);
}

function add_feed(feed){
    for(let blog of feed){
        feedContainer.innerHTML += `
            <a href="${blogUrl}${blog.id}/" class="blog-link">
                <div class="blog">
                    <h2 class="blog-title">${blog.title}</h2>
                    <p class="blog-tags">Tags: ${blog.tags}</p>
                    <div class="blog-meta">
                        <span class="blog-author">Author: ${blog.author}</span>
                        <span class="blog-time">${updateTime(blog.date_of_pub)}</span>
                    </div>
                </div>
            </a>`;
    }
}

function loadFeed(){
    let feedPromice = get_feed();
    feedPromice.then((response) => response.json())
    .then((data) => {
        add_feed(data.results);
        if(data.next == ""){
            loadMoreButton.style.display = "none";
        }
        nextURL.value = data.next;
        takeNextUrl = false;
    })
    .catch((error) => {
        console.log(error);
    });
}

document.addEventListener('DOMContentLoaded',() => {

    preferenceToggle.addEventListener('click',() => {
        if(personalized){
            personalized = false;
        }else{
            personalized = true;
        }
    })
    
    loadFeed();
    
    reloadButton.addEventListener('click',() => {
        feedContainer.innerHTML = "";
        loadFeed();
    });

    loadMoreButton.addEventListener('click',() => {
        takeNextUrl = true;
        loadFeed();
    });

});
    