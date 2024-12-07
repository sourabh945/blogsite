document.addEventListener("DOMContentLoaded", () => {
    const childDiv = document.getElementById("card-front");
    const parentDiv = document.getElementById("card");
  
    // Function to adjust the parent div's height
    function adjustParentHeight() {
      const childHeight = childDiv.scrollHeight;
      parentDiv.style.height = `${childHeight}px`;
      console.log(childHeight);
    }
  
    // Initial adjustment on page load
    adjustParentHeight();
  });
  