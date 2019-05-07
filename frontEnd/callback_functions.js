const factor = 10

function drawBasic(data) {
  var table = new google.visualization.DataTable();
  table.addColumn('number', 'Plays');
  table.addColumn('number', `Probability of ${data[0]['away']} Win`);

  var arr = data[0]['play-by-play']
  var prob_array = arr.map(function(elem, index) {
    if(index == 0)
      return null
    return [index, elem]
  })

  table.addRows(prob_array);

  var options = {
    hAxis: {
      title: 'Plays'
    },
    vAxis: {
      title: `Probability of ${data[0]['away']} Win`
    }
  }

  var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

  chart.draw(table, options);
}

// Display an error in the error_banner.
// Adding an error to the error_banner will remove any previous errors,
// though they will be logged.

function display_error(statusCode) {
  var errorDiv = document.getElementById('error_banner')
  var errorMessage = document.createElement('p')

  console.log('Something went wrong. Error: ' + statusCode)

  if(errorDiv) {
    errorDiv.innerHTML = ''

    errorMessage.textContent = 'Something went wrong. Error: ' + statusCode
    errorMessage.id = 'errorID'
    errorDiv.appendChild(errorMessage)
  }
  else {
    console.log('Error: Cannot find the error banner.')
  }
}

// Make sure the request went through.
// If it did, call the function.
// Otherwise, display an error.

function onload_wrapper(f, request, response) {
  if (request.status >= 200 && request.status < 400) {
    var response = JSON.parse(response)
    var data = response.data
    var yearweek = response.yearweek
    f(response, data)  
  }
  else {
    display_error(request.status)
  }
}

function onload_generate_graph(response, data) {
  google.charts.load('current', {packages: ['corechart', 'line']});
  google.charts.setOnLoadCallback(function() { drawBasic(data) });
}

function calculate_new_score(top_score, score) {
  return 100*Math.pow(factor, 1+15*score)/top_score
}

function onload_generate_list(response, data) {
  var container = document.getElementById('list_div')

  if(container != null) {

    if(data != "") {
      var ol = document.createElement('ol')
      var num = 1
      var top_score = Math.pow(factor, 1+15*data[0].score)
      var span = null
      var p = null
      var score = null
      var split_date = response.yearweek.split(':')

      data.forEach(game => {
        // This is wrapped in a function so that we can create a closure.
        // Otherwise, li.id will change and we will create the wrong line chart.
        (function() {
          var li = null

          li = document.createElement('li')
          li.id = `${game.score}:${game.home}`
          li.onclick = function() { create_linechart(li.id) }

          span = document.createElement('span')
          span.textContent = num++

          p = document.createElement('p')

          score = calculate_new_score(top_score, game.score)

          p.textContent = `${game.away} vs. ${game.home} : ${score}`

          li.appendChild(span)
          li.appendChild(p)
          ol.appendChild(li)
        })()

      })

      // Give ol some properties that we can refer back to for caching purposes.
      ol.id = 'list_of_games'
      ol.setAttribute('year', split_date[0])
      ol.setAttribute('week', split_date[1])

      container.innerHTML = ''
      container.appendChild(ol)
    }
    else {
      const errorMessage = document.createElement('p')
      errorMessage.textContent = `We don't have data for that week.`
      errorMessage.id = 'errorID'
      app.appendChild(errorMessage)            
    }
  } 
}