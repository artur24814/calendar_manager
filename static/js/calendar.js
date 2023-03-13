console.log('ok')

const active_d = document.querySelectorAll('.active-d')
const timeline = document.querySelector('.timeline-col')
const timeline_body = document.querySelector('.timeline')
const form_ask_meeting = document.querySelector('#form-ask-meeting')


for (element of active_d){
    element.addEventListener('click', function(){
        let month = this.dataset.month;
        let day = this.dataset.day;
        let userID = this.dataset.pk;

        console.log('month:', month, 'day:', day , 'userId:',userID)

        getDayMeetingInfo(month, day, userID)
        timeline.classList.remove('col-hide')
        if (form_ask_meeting !== null ){
        form_ask_meeting.action = `/calendar/timeline-for-followers/${month}/${day}/${userID}/`;
    }
    })
}

function getDayMeetingInfo(month,day, userID){
    var url = '/calendar/info-timeline/'

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
            console.log(data)
			console.log(data.meetings)
            console.log(data.month)
            if ((data.meetings).length === 0 ){
                timeline_body.innerHTML = `<div class="text-center"><h1> Free Day 😎 </h1></div>`
            } else {
                timeline_body.innerHTML = `<div class="text-center"><h1> ${data.meetings[0].date}</h1></div>`
                for (meeting of data.meetings){
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
								<span class="badge rounded-pill bg-secondary">${meeting.asker.name}</span>
								<span class="badge rounded-pill bg-success">${meeting.replied.name}</span>
							</div>
                        </div>
                    </div>
                    `
                    }
                }
            } 
		});
}