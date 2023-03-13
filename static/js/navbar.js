const nav = document.querySelector('#nav');
const meeting_quantity = document.querySelector('#meeting-quantity')
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

meeting_quantity.addEventListener('click', function(){
    let meetings = this.dataset.meetings
    console.log(meetings)
    let htmlContent = ''
    for (element in meetings){
        htmlContent += `<div class="alert alert-primary" role="alert">
                            ${element}.
                        </div>`
    }
    Swal.fire({
        title: 'Your meetings',
        icon: 'info',
        html: htmlContent,
        showCloseButton: true,
        focusConfirm: false,
        confirmButtonText:
            '<i class="fa fa-thumbs-up"></i> Great!',
        confirmButtonAriaLabel: 'Thumbs up, great!',
        })
})