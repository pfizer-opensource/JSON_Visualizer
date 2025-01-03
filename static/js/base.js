document.addEventListener("DOMContentLoaded", () => {
  const hamburgerMenu = document.querySelector("#hamburger-menu");
  const overlay = document.querySelector("#overlay");
  const nav1 = document.querySelector("#nav-1");
  const nav2 = document.querySelector("#nav-2");

  const navItems = [nav1, nav2];

  // Control Navigation Animation
  function navAnimation(val1, val2) {
    navItems.forEach((nav, i) => {
      nav.classList.replace(`slide-${val1}-${i + 1}`, `slide-${val2}-${i + 1}`);
    });
  }

  function toggleNav() {
    console.log('Toggling navigation');
    // Toggle: Hamburger Open/Close
    hamburgerMenu.classList.toggle("active");

    // Toggle: Menu Active
    overlay.classList.toggle("overlay-active");
    console.log('Overlay active:', overlay.classList.contains("overlay-active"));

    if (overlay.classList.contains("overlay-active")) {
      // Animate In - Overlay
      overlay.classList.replace("overlay-slide-left", "overlay-slide-right");

      // Animate In - Nav Items
      navAnimation("out", "in");
    } else {
      // Animate Out - Overlay
      overlay.classList.replace("overlay-slide-right", "overlay-slide-left");

      // Animate Out - Nav Items
      navAnimation("in", "out");
    }
  }

  // Events Listeners
  hamburgerMenu.addEventListener("click", toggleNav);
  navItems.forEach((nav) => {
    nav.addEventListener("click", toggleNav);
  });
});

const dropContainer = document.getElementById("dropcontainer")
  const fileInput = document.getElementById("json_")

  dropContainer.addEventListener("dragover", (e) => {
    // prevent default to allow drop
    e.preventDefault()
  }, false)

  dropContainer.addEventListener("dragenter", () => {
    dropContainer.classList.add("drag-active")
  })

  dropContainer.addEventListener("dragleave", () => {
    dropContainer.classList.remove("drag-active")
  })

  dropContainer.addEventListener("drop", (e) => {
    e.preventDefault()
    dropContainer.classList.remove("drag-active")
    fileInput.files = e.dataTransfer.files
  })


