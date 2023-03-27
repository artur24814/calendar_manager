const nav = document.querySelector('#nav');
const meeting_quantity = document.querySelector('#meeting-quantity')


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

//Open meeting modal
meeting_quantity.addEventListener('click', function(){
    let meetings = JSON.parse(this.dataset.meetings)
    let url = this.dataset.url
    let user_id = this.dataset.user

    let htmlContent = ''
    for (index in meetings){
        let element = meetings[index]
        if (element.confirmed === false && element.replied.id == user_id){
            htmlContent += 
            `<div class="alert alert-primary" role="alert">
                <a href="${url}${element.id}" data-bs-toggle="tooltip" data-bs-placement="top" title="Click to accept meeting"
                onclick="return confirm(Are you sure accept meeting with ${element.asker.name} at ${element.time_start} ${element.date} ?);">
                    <img class='m-image' src="https://img.icons8.com/external-bearicons-blue-bearicons/64/null/external-question-call-to-action-bearicons-blue-bearicons.png" width="24" height="24"/>
                </a>
                <div>
                    ${element.time_start} - ${element.time_start}  <br>
                    Between: ${element.asker.name} and ${element.replied.name} <br>
                    ${element.date}
                </div>
            </div>`
        } else if (element.confirmed === true) {
            htmlContent +=
            `<div class="alert alert-primary" role="alert">
                <img class='m-image' src="https://img.icons8.com/doodle/48/null/checkmark.png" width="30" height="30"/>
                &nbsp&nbsp
                <div>
                    ${element.time_start} - ${element.time_start}  <br>
                    Between: ${element.asker.name} and ${element.replied.name} <br>
                    ${element.date}
                </div>
            </div>`
        } else {
            htmlContent += 
            `<div class="alert alert-primary" d-flex role="alert">
                <div>
                    <img class='m-image' src="https://img.icons8.com/external-bearicons-blue-bearicons/64/null/external-question-call-to-action-bearicons-blue-bearicons.png" width="24" height="24"/>
                        &nbsp&nbsp
                    ${element.time_start} - ${element.time_finish} <br>
                        Between:${element.asker.name} and ${element.replied.name}
                        ${element.date}
                </div>
            </div>`
        }
    }
    Swal.fire({
        title: 'Your meetings',
        icon: 'info',
        width: 800,
        html: htmlContent,
        showCloseButton: true,
        focusConfirm: false,
        confirmButtonText:
            '<i class="bi bi-hand-thumbs-up"></i> Great!',
        confirmButtonAriaLabel: 'Thumbs up, great!',
    })
})
