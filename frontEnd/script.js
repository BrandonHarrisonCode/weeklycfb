const lambdaURL = 'https://6c1yu4c5lj.execute-api.us-east-1.amazonaws.com/Prod/'
// const lambdaURL = 'https://fchv75rdm1.execute-api.us-east-1.amazonaws.com/default/travisAccessLambda'
const app = document.getElementById('list_div')

//Create dropdown menus
const year_dropdown = document.getElementById('year_dropdown')
const week_dropdown = document.getElementById('week_dropdown')

function create_linechart(score, awayTeamName) {
  var listOfGames = document.getElementById('list_of_games')
  var chartDiv = document.getElementById('chart_div')
  var request = new XMLHttpRequest()

  // TODO Return some error if listOfGames cannot be found
  if(chartDiv != null) {
    // Set this so we can make sure that we picked the right game later. 
    // Used in the unlikely case two games have the same score.
    chartDiv.setAttribute('away', awayTeamName)
    if(listOfGames != null) {

      request.open('GET', lambdaURL + '?year=' + listOfGames.getAttribute('year') + '&week=' + listOfGames.getAttribute('week') + '&score=' + score, true)
      request.onload = function() { onload_wrapper(onload_generate_graph, request, this.response) }
      request.send()
    }
  }
}

function retrieve_availible_weeks() {
    var request = new XMLHttpRequest();
    request.open('GET', lambdaURL + 'availibleWeeks', true)
    request.onload = function() { onload_wrapper(onload_populate_dropdowns, request, this.response)}
    request.send()
}

function retrieve_weeks_data() {
  var request = new XMLHttpRequest()
  request.open('GET', lambdaURL + 'entertainmentScores?year=' + year_dropdown.value + '&week=' + week_dropdown.value, true)
  request.onload = function() { onload_wrapper(onload_generate_list, request, this.response)}
  request.send()
}

retrieve_availible_weeks()
