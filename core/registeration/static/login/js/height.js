document.addEventListener("DOMContentLoaded", () => {
    const childDiv = document.getElementById("card-front");
    const parentDiv = document.getElementById("card");

    const flipButton = document.getElementById('signup-flip-button');
    const flipButtonBack = document.getElementById('login-flip-button');
  
    // Function to adjust the parent div's height
    function adjustParentHeight() {
      const childHeight = childDiv.scrollHeight;
      parentDiv.style.height = `${childHeight}px`;
      console.log(childHeight);
    }
  
    // MutationObserver to watch for changes in child div's content
    const observer = new MutationObserver(() => {
      adjustParentHeight();
    });
  
    // Start observing changes in the child div
    observer.observe(childDiv, {
      childList: true,    // Watches for child nodes being added or removed
      subtree: true,      // Watches all descendant nodes
      characterData: true // Watches changes to text content
    });
  
    // Listen to input events in case of user typing (for contenteditable)
    childDiv.addEventListener("input", adjustParentHeight);

    flipButton.addEventListener('click',adjustParentHeight);
    flipButtonBack.addEventListener('click',adjustParentHeight);


  
    // Initial adjustment on page load
    adjustParentHeight();
  });
  