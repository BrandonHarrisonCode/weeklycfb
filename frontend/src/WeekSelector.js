import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import 'typeface-roboto';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';

const useStyles = theme => ({
  dateSelector: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.background.paper,
    borderRadius: 4,
    padding: '.05em .13em .05em .06em',
  },
  yearSelector: {
    width: '10ch',
  },
  weekSelector: {
    marginRight: theme.spacing(3),
    width: '8ch',
  },
}); 

function descendingIntegerSort(array) {
  return array.sort(function(a,b) {return a - b;}).reverse();
}

class WeekSelector extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      years: [],
    };
  }

  async componentDidMount() {
    this.setState({
      years: [], 
    });

    this.fetchAvailibleWeeks();
  }

  async fetchAvailibleWeeks() {
    const url = 'https://api.cfbgameoftheweek.com/availibleWeeks'
    const response = await fetch(url);
    const parsedJSON = await response.json();

    this.setState({
      years: parsedJSON.data, 
    });
  }

  handleYearChange(event) {
    this.props.handleYearChange(event.target.value);
  }

  handleWeekChange(event) {
    this.props.handleWeekChange(event.target.value);
  }

  render() {
    const classes = this.props.classes;
    const years = this.state.years;
    const weeks = this.state.years[this.props.year] ? this.state.years[this.props.year] : [];

    return (
      <div>
          <TextField
            select
            value={Object.keys(years).includes(this.props.year.toString()) ? this.props.year : ''}
            id="yearSelect"
            label="Year"
            variant="filled"
            onChange={this.handleYearChange.bind(this)}
            className={`${classes.dateSelector} ${classes.yearSelector}`}
            margin="dense"
          >
            {
              descendingIntegerSort(Object.keys(years)).map(year => {
                return <MenuItem key={year} value={year}>{year}</MenuItem>;
              })
            }
          </TextField>
          <TextField
            select
            value={weeks.includes(this.props.week.toString()) ? this.props.week : ''}
            id="weekSelect"
            label="Week"
            variant="filled"
            onChange={this.handleWeekChange.bind(this)}
            className={`${classes.dateSelector} ${classes.weekSelector}`}
            margin="dense"
          >
            {
              descendingIntegerSort(weeks).map(week => {
                return <MenuItem key={week} value={week}>{week}</MenuItem>;
              })
            }
          </TextField>
      </div>
    );
  }
}

export default withStyles(useStyles)(WeekSelector);
