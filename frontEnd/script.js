const factor = 10

const app = document.getElementById('root')

//Create dropdown menus
const year_dropdown = document.getElementById('year_dropdown')
const week_dropdown = document.getElementById('week_dropdown')

var year_list = ["2017", "2018"]
var option_text
for(option_text in year_list) {
  var option = document.createElement("option")
  option.text = year_list[option_text]
  year_dropdown.add(option)
}

for(var i = 1; i < 17; i++) {
  var option = document.createElement("option")
  option.text = i
  week_dropdown.add(option)
}

const container = document.createElement('div')
container.setAttribute('class', 'container')

app.appendChild(container)


function calculate_new_score(top_score, score) {
  return 100*Math.pow(factor, 1+15*score)/top_score
}

function retrieve_data() {
  var request = new XMLHttpRequest()
  request.open('GET', 'https://fchv75rdm1.execute-api.us-east-1.amazonaws.com/default/travisAccessLambda?year=' + year_dropdown.value + '&week=' + week_dropdown.value, true)
  request.onload = function() {
    // Clear the old content. Apparently this is faster in Chrome now.
    var shownError = document.getElementById('errorID')
    if(shownError != null)
      shownError.parentNode.removeChild(shownError)
    container.innerHTML = ''

    if (request.status >= 200 && request.status < 400) {
      // Begin accessing JSON data here
      var data = JSON.parse(this.response)


      if(data != "") {
        const ol = document.createElement('ol')
        var num = 1
        var top_score = Math.pow(factor, 1+15*data[0].score)
        data.forEach(game => {

          const li = document.createElement('li')
          const span = document.createElement('span')
          span.textContent = num++

          const p = document.createElement('p')

          var score = calculate_new_score(top_score, game.score)

          p.textContent = `${game.away} vs. ${game.home} : ${score}`



          li.appendChild(span)
          li.appendChild(p)
          ol.appendChild(li)
        })
        container.appendChild(ol)
      }
      else {
        const errorMessage = document.createElement('p')
        errorMessage.textContent = `We don't have data for that week.`
        errorMessage.id = 'errorID'
        app.appendChild(errorMessage)            
      }
    } else {
      const errorMessage = document.createElement('p')
      errorMessage.textContent = `Something went wrong.`
      errorMessage.id = 'errorID'
      app.appendChild(errorMessage)
    }
  }
  request.onerror = request.onload
  request.send()
}

retrieve_data()