import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import 'typeface-roboto';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
//import InputLabel from '@material-ui/core/InputLabel';
//import Select from '@material-ui/core/Select';
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

class WeekSelector extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      year: 2019,
      week: 1,
    };
  }

  handleChangeYear(event, newValue) {
    this.setState({
      year: event.target.value,
    });
  }

  handleChangeWeek(event, newValue) {
    this.setState({
      week: event.target.value,
    });
  }


  render() {
    const classes = this.props.classes;
    return (
      <div>
          <TextField
            select
            value={this.state.year}
            id="yearSelect"
            label="Year"
            variant="filled"
            onChange={this.handleChangeYear.bind(this)}
            className={`${classes.dateSelector} ${classes.yearSelector}`}
            margin="dense"
          >
            <MenuItem value="2019">2019</MenuItem>
            <MenuItem value="2018">2018</MenuItem>
            <MenuItem value="2017">2017</MenuItem>
          </TextField>
          <TextField
            select
            value={this.state.week}
            id="weekSelect"
            label="Week"
            variant="filled"
            onChange={this.handleChangeWeek.bind(this)}
            className={`${classes.dateSelector} ${classes.weekSelector}`}
            margin="dense"
          >
            <MenuItem value="1">1</MenuItem>
            <MenuItem value="2">2</MenuItem>
            <MenuItem value="3">3</MenuItem>
            <MenuItem value="10">10</MenuItem>
          </TextField>
      </div>
    );
  }
}

export default withStyles(useStyles)(WeekSelector);
