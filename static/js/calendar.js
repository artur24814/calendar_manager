const active_d = document.querySelectorAll('.active-d')
const timeline = document.querySelector('.timeline-col')
const timeline_body = document.querySelector('.timeline')
const form_ask_meeting = document.querySelector('#form-ask-meeting')

//Get curent day
const date = new Date()
let currentDay = date.getDate()


//Add Event Lisner to clicked date
for (element of active_d){
    element.addEventListener('click', function(){
        let month = this.dataset.month;
        let day = this.dataset.day;
        let userID = this.dataset.pk;
        let calendar_url = this.dataset.calendarurl

        console.log('month:', month, 'day:', day , 'userId:',userID)

        getDayMeetingInfo(month, day, userID, calendar_url)

        //show Timeline
        timeline.classList.remove('col-hide')
        //if form is null thats mean this view for user himself
        if (form_ask_meeting !== null ){

        //change action for particular url  
        form_ask_meeting.action = `/calendar/timeline-for-followers/${month}/${day}/${userID}/`;

        //if Day in a past hide form 
        if (currentDay > day){
            form_ask_meeting.classList.add('d-none')
        } else {
            form_ask_meeting.classList.remove('d-none') 
        }
    }
    })
}

function getDayMeetingInfo(month,day, userID, calendar_url){
    var url = '/calendar/info-timeline/'
        //if sing_in not null it is mean user is not login, redirect to login
        const sing_in = document.querySelector('#sing-in')
        if (sing_in !== null){
            let redirect_url = sing_in.dataset.redirecturl
            console.log(redirect_url)
            window.location.replace(redirect_url);
        }
        // send request
		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'month':month, 'day': day,'userId':userID})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
            if ((data.meetings).length === 0 ){
                timeline_body.innerHTML = `<div class="text-center"><h1> Free Day 😎 </h1></div>`
            } else {
                timeline_body.innerHTML = `<div class="text-center"><h1> ${data.meetings[0].date}</h1></div>`
                for (meeting of data.meetings){
                    // if show detail undefined it is mean this view for guests
                    if (data.show_detail === undefined ){
                    console.log(meeting)
                    timeline_body.innerHTML += 
                    `<div class="timeline-row">
                        <div class="timeline-time">
                            ${meeting.time_start}
                        </div>
                        <div class="timeline-content">
                            <i class="icon-attachment"></i>
                            <h4>${meeting.title}</h4>
                            <p>From: ${(meeting.time_start).slice(0, -3)} to ${meeting.time_finish}</p>
                        </div>
                    </div>
                    `
                    } else {
                        timeline_body.innerHTML += 
                    `<div class="timeline-row">
                        <div class="timeline-time">
                            ${meeting.time_start}
                        </div>
                        <div class="timeline-content">
                            <i class="icon-attachment"></i>
                            <h4>${meeting.title}</h4>
                            <p>From: ${(meeting.time_start).slice(0, -3)} to ${meeting.time_finish}</p>
                            <div class="thumbs">
								<img class="img-fluid rounded" src="${meeting.asker.img_url}" alt="${meeting.asker.name}">
								<img class="img-fluid rounded" src="${meeting.replied.img_url}" alt="${meeting.replied.name}">
							</div>
                            <div class="thumbs">
                                <a href="${calendar_url}${meeting.asker.id}">
                                    <span class="badge rounded-pill bg-secondary">${meeting.asker.name}</span>
                                </a>
                                <a href="${calendar_url}${meeting.replied.id}">
								    <span class="badge rounded-pill bg-success">${meeting.replied.name}</span>
                                </a>
							</div>
                        </div>
                    </div>
                    `
                    }
                }
            } 
		});
}