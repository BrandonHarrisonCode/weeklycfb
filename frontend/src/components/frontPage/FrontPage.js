import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import TabPanel from '../common/TabPanel';
import WeekSelector from './weekSelector'
import CardList from './cards/CardList';

const useStyles = theme => ({
  title: {
    margin: '1em .2em .2em .2em',
    color: '#4f6d7a',
  },
}); 


class FrontPage extends TabPanel {
  constructor(props) {
    super(props);
    this.handleYearChange = this.handleYearChange.bind(this);
    this.handleWeekChange = this.handleWeekChange.bind(this);

    this.state = {
      year: '2019',
      week: '1',
    };
  }

  handleYearChange(value) {
    this.setState({year: value});
  }

  handleWeekChange(value) {
    this.setState({week: value});
  }

  render() {
    const classes = this.props.classes;
    const year = this.state.year;
    const week = this.state.week;

    if(this.props.currentTabName !== this.props.tabName) {
      return null;
    }
    return (
      <Grid
        container
        spacing={0}
        direction="column"
        alignItems="center"
        justify="flex-start"
      >
        <Grid item xs={12}>
          <Typography 
            variant="h2" 
            component="h1" 
            className={classes.title}
            align="center"
          >
            CFB Game of the Week
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <WeekSelector 
            year={this.state.year}
            week={this.state.week}
            handleYearChange={this.handleYearChange} 
            handleWeekChange={this.handleWeekChange}
          />
        </Grid>
        <Grid item xs={12}>
          <CardList year={year} week={week}/>
        </Grid>
      </Grid>
    );
  }
}

export default withStyles(useStyles)(FrontPage);
