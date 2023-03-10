console.log('ok')

const active_d = document.querySelectorAll('.active-d')
const timeline = document.querySelector('.timeline-col')
const timeline_body = document.querySelector('.timeline')


for (element of active_d){
    element.addEventListener('click', function(){
        let month = this.dataset.month
        let day = this.dataset.day
        let userID = this.dataset.pk

        console.log('month:', month, 'day:', day , 'userId:',userID)

        getDayMeetingInfo(month, day, userID)
        timeline.classList.remove('col-hide')

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
            if (data.form === true ) {
                timeline.innerHTML = 
                `<div class="card" style="background: rgba( 255, 255, 255, 0.6 );
                            padding: 10px;
                            backdrop-filter: blur( 7px );
                            -webkit-backdrop-filter: blur( 7px );
                            border: 1px solid rgba(107,94,94,0.18);
                            -webkit-box-shadow: -1px -3px 24px 0px rgb(146,147,161);
                            -moz-box-shadow: -1px -3px 24px 0px rgb(176,177,183);
                            box-shadow: 10px 3px 24px 0px rgba(66, 68, 90, 10);">
                    <form>
                        <div class="mb-3">
                            <label for="exampleInputEmail1" class="form-label">Email address</label>
                            <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
                            <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
                        </div>
                        <div class="mb-3">
                            <label for="exampleInputPassword1" class="form-label">Password</label>
                            <input type="password" class="form-control" id="exampleInputPassword1">
                        </div>
                        <div class="mb-3 form-check">
                            <input type="checkbox" class="form-check-input" id="exampleCheck1">
                            <label class="form-check-label" for="exampleCheck1">Check me out</label>
                        </div>
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </form>
                </div>`
            } if ((data.meetings).length === 0 ){
                timeline.innerHTML += `<div class="timeline-row"><h1> Empty </h1></div>`
            } else {
                    timeline.innerHTML += 
                    `<div class="timeline-row">
                        <div class="timeline-time">
                            sdg- sdg
                        </div>
                        <div class="timeline-content">
                            <i class="icon-attachment"></i>
                            <h4>Meeting</h4>
                            <p>Hello</p>
                            <div class="thumbs">
                                <img class="img-fluid rounded" src="" alt="Maxwell Admin">
                                <img class="img-fluid rounded" src="" alt="Maxwell Admin">
                            </div>
                            <div class="">
                                <span class="badge badge-pill">gj gh</span>
                                <span class="badge badge-pill">sdf sdfgg</span>
                            </div>
                        </div>
                    </div>
                    `
            } 
		});
}