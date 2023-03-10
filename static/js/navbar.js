const nav = document.querySelector('#nav');
console.log('ok')

const onScroll = (event) => {
    const scrollPosition = event.target.scrollingElement.scrollTop;
    if (scrollPosition > 10) {
        if (
            !nav.classList.contains('scrolled-down')
        ){
            nav.classList.add('scrolled-down');
        }
    } else {
        if (
            nav.classList.contains('scrolled-down')
        ) {
            nav.classList.remove('scrolled-down');
        }
    }
};

document.addEventListener('scroll', onScroll);

// Nav hamburgerburger selections

const burger = document.querySelector("#burger-menu");
const ul = document.querySelector(".links");

burger.addEventListener("click", () => {
    ul.classList.toggle("show");
  });

// Close hamburger menu when a link is clicked

// Select nav links
const navLink = document.querySelectorAll(".nav-link");

navLink.forEach((link) =>
  link.addEventListener("click", () => {
    ul.classList.remove("show");
  })
);