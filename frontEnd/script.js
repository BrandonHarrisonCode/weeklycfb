const app = document.getElementById('list_div')
const lambdaURL = 'https://fchv75rdm1.execute-api.us-east-1.amazonaws.com/default/travisAccessLambda'

//Create dropdown menus
const year_dropdown = document.getElementById('year_dropdown')
const week_dropdown = document.getElementById('week_dropdown')

// TODO make these build via function calls for easy change to dynamic build later
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


function create_linechart(score) {
  var listOfGames = document.getElementById('list_of_games')

  // TODO Return some error if listOfGames cannot be found
  if(listOfGames != null) {
    var request = new XMLHttpRequest()

    request.open('GET', lambdaURL + '?year=' + listOfGames.getAttribute('year') + '&week=' + listOfGames.getAttribute('week') + '&score=' + score, true)
    request.onload = function() { onload_wrapper(onload_generate_graph, request, this.response) }
    request.send()
  }
}

function retrieve_data() {
  var request = new XMLHttpRequest()
  request.open('GET', lambdaURL + '?year=' + year_dropdown.value + '&week=' + week_dropdown.value, true)
  request.onload = function() { onload_wrapper(onload_generate_list, request, this.response)}
  request.send()
}

retrieve_data()