const factor = 10
const genericError = 'Something went wrong. Please try again.'
const replaceErrorString = 'ELEM'
const cannotFindElementError = 'The element ' + replaceErrorString + ' could not be found. Please try refreshing.'
const cannotFindErrorBannerError = 'The error banner could not be found. Please try refreshing.'
const listDivId = 'list_div'
const chartDivId = 'chart_div'
const errorBannerId = 'error_banner'
const gameListId = 'list_of_games'

var yearweeks = null;
var winProbabilityData = {}

function generate_graph(game) {
    winProbabilityData = game;
    google.charts.load('current', {packages: ['corechart', 'line']})
    google.setOnLoadCallback(draw_win_probability_graph);
}

function draw_win_probability_graph() {
  var awayTeamName = winProbabilityData.awayTeamName;
  var homeTeamName = winProbabilityData.homeTeamName;
  var playByPlay = winProbabilityData.playByPlay;

  var table = new google.visualization.DataTable()
  var chart = new google.visualization.LineChart(document.getElementById(chartDivId))

  if(winProbabilityData != null && table != null && chart != null) {
    var splitDate = winProbabilityData.splitdate;

    // Create an array of arrays of the form [playNumber, winProbabilityForAwayTeam]
    // Note that the 0th play is dropped because all teams start with a 50/50 chance of winning.
    var probabilityData = playByPlay.map(function(winProbabilityForAwayTeam, playNumber) {
      if(playNumber == 0)
        return null
      return [playNumber, winProbabilityForAwayTeam]
    })

    table.addColumn('number', 'Plays')
    table.addColumn('number', `Probability of ${awayTeamName} Win`)
    table.addRows(probabilityData)

    var intervals = Math.floor(probabilityData.length/50) + 1
    var horizontalTickList = new Array(intervals)
    for(var i = 0; i < intervals; i++) {
      horizontalTickList[i] = { v: 50*i}
    }
    horizontalTickList[intervals] = {v: probabilityData[probabilityData.length-1][0]}

    var options = {
      fontName: 'Lato',
      fontSize: 12,
      title: `${awayTeamName} at ${homeTeamName}\nWeek ${splitDate[1]} of ${splitDate[0]}`,
      titleTextStyle: { 
        color: 'black',
        fontName: 'Lato',
        fontSize: 15,
      },
      legend: 'none',

      hAxis: {
        ticks: horizontalTickList,
        title: 'Plays',
      },
      vAxis: {
        ticks: [0, 0.25, 0.50, 0.75, 1.0],
        viewWindow: {
          max: 1.0
        },
        title: `Probability of ${awayTeamName} Win`,
        format: '0.00',
        allowContainerBoundaryTextCufoff: true
      },
      lineWidth: 3,
      chartArea: {'left': '10%', 'bottom': '20%', 'top': '10%', 'right': '5%', 'width': '90%', 'height': '100%'},
      width: "100%",
      height: "100%",
      colors: ['#118AB2'],
      animation: {
        startup: true,
        duration: 1000,
        easing: 'out'
      }
      // trendlines: {
      //   0: {
      //     type: 'polynomial',
      //     n: {
      //       degree: -1
      //     },
      //     color: 'green',
      //     lineWidth: 3,
      //     opacity: 0.3,
      //     showR2: true,
      //     visibleInLegend: false
      //   }
      // }
    }

    chart.draw(table, options)
    // And then:
    $(window).smartresize(function () {
      chart.draw(table, options);
    });

  }
  else {
    display_element_missing_error(chartDivId)
  }
}

function display_element_missing_error(missingElementId) {
  display_error(statusCode=null, errorText=cannotFindElementError.replace(replaceErrorString, missingElementId))
}

// Display an error in the error_banner.
// Adding an error to the error_banner will remove any previous errors,
// though they will be logged.

function display_error(statusCode='', errorText=genericError) {
  var errorDiv = document.getElementById(errorBannerId)
  var errorMessage = document.createElement('p')

  if(statusCode != '')
    statusCode = ` Error Code: $statusCode`

  console.log(errorText + statusCode)

  if(errorDiv != null) {
    errorDiv.innerHTML = ''

    errorMessage.textContent = errorText + statusCode
    errorDiv.appendChild(errorMessage)
  }
  else {
    console.log(cannotFindErrorBannerError)
  }
}

// Make sure the request went through.
// If it did, call the function.
// Otherwise, display an error.

function onload_wrapper(f, request, response) {
  if (request.status >= 200 && request.status < 400) {
    var response = JSON.parse(response)
    var data = response.data
    f(response, data)  
  }
  else {
    display_error(request.status)
  }
}

function calculate_new_score(top_score, score) {
  return 100*Math.pow(factor, 1+15*score)/top_score
}

function onload_populate_dropdowns(response, data) {
    yearweeks = data;

    populate_dropdowns();
}

function populate_dropdowns() {
    var yearDropdown = document.getElementById('year_dropdown');
    var weekDropdown = document.getElementById('week_dropdown');
    weekDropdown.innerHTML = '';

    if(yearDropdown.options.length == 0) {
        var option_text
        for(option_text in yearweeks) {
            var option = document.createElement("option")
            option.text = option_text
            year_dropdown.add(option);
        }
    }

    yearweeks[year_dropdown.value].forEach(function(value) {
        var option = document.createElement("option")
        option.text = value
        week_dropdown.add(option)
    });
    
    retrieve_weeks_data();
}

function onload_generate_list(response, data) {
  var listDiv = document.getElementById(listDivId)

  if(listDiv != null) {

    if(data != "") {
      var ol = document.createElement('ol')
      var num = 0
      var top_score = Math.pow(factor, 1+15*data[0].score)
      var span = null
      var p = null
      var score = null
      var split_date = response.yearweek.split(':')

      data.forEach(game => {
        // This is wrapped in a function so that we can create a closure.
        // Otherwise, li.id will change and we will create the wrong line chart.
        var li = null

        li = document.createElement('li')
        li.onclick = function() { create_linechart(game.score, game.away) }
        li.onclick = function() { generate_graph({'splitdate': split_date, 'homeTeamName': game.home, 'awayTeamName': game.away, 'playByPlay': game['play-by-play']})}
        li.setAttribute('page', Math.floor(num/7))
        li.setAttribute('play-by-play', game['play-by-play']);

        // Only things on the first page should be shown.
        if(li.getAttribute('page') != '0')
          li.style.display = 'none'

        span = document.createElement('span')
        span.textContent = ++num

        p = document.createElement('p')

        score = calculate_new_score(top_score, game.score)

        p.innerHTML = `<strong>${game.away} @ ${game.home}</strong> &emsp; Our Score: ${Math.round(score)}`

        li.appendChild(span)
        li.appendChild(p)
        ol.appendChild(li)
      })

      // Give ol some properties that we can refer back to for caching purposes.
      ol.id = gameListId
      ol.setAttribute('page', 0)
      ol.setAttribute('year', split_date[0])
      ol.setAttribute('week', split_date[1])

      listDiv.innerHTML = ''
      var listTitle = document.createElement('h1')
      listTitle.innerHTML = `Game Ranking for Week ${split_date[1]} of ${split_date[0]}`
      listTitle.id = 'list_title'

      listDiv.appendChild(listTitle)
      listDiv.appendChild(ol)
      set_button_visibility(0, ol.childNodes.length)
    }
    else {
      var errorDiv = document.getElementById(errorBannerId)
      var errorMessage = document.createElement('p')
      errorDiv.innerHTML = ''
      errorMessage.textContent = 'There is no data for that week.'
      errorDiv.appendChild(errorMessage)            
    }
  } 
  else {
    display_element_missing_error(listDivId)
  }
}

function set_button_visibility(currentPage, numberOfGames) {
  var nextButton = document.getElementById('next_button')
  var backButton = document.getElementById('back_button')

  if(currentPage <= 0)
    backButton.style.visibility = 'hidden'
  else
    backButton.style.visibility = 'visible'

  if(currentPage >= Math.ceil(numberOfGames/7) - 1)
    nextButton.style.visibility = 'hidden'
  else
    nextButton.style.visibility = 'visible'
}


function change_page(numberToChange) {
  var listOfGames = document.getElementById(gameListId)

  if(listOfGames != null) {
    var currentPageNumber = parseInt(listOfGames.getAttribute('page'), 10)
    var newPageNumber = currentPageNumber + numberToChange
    var numberOfGames = listOfGames.childNodes.length

    listOfGames.setAttribute('page', newPageNumber)
    listOfGames.querySelectorAll(`[page='${currentPageNumber}']`).forEach( game => {
        game.style.display = 'none'
    })
    listOfGames.querySelectorAll(`[page='${newPageNumber}']`).forEach( game => {
        game.style.display = 'list-item'
    })
    set_button_visibility(newPageNumber, numberOfGames)
  }
  else {
    display_element_missing_error(gameListId)
  }
}


function next_page() {
  change_page(1)
}

function prev_page() {
  change_page(-1)
}
