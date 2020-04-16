import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
//import './FrontPage.css'
import TabPanel from './TabPanel';
import WeekSelector from './WeekSelector'
import CardList from './CardList';

const useStyles = theme => ({
  title: {
    padding: '1em 5px 5px 1em',
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

    return (
      <Grid
        container
        spacing={0}
        direction="column"
        alignItems="center"
        justify="center"
        style={{ minHeight: '100vh' }}
      >
       <Typography variant="h3" component="h1" className={classes.title}>CFB Game of the Week</Typography>
        <WeekSelector 
              year={this.state.year}
              week={this.state.week}
              handleYearChange={this.handleYearChange} 
              handleWeekChange={this.handleWeekChange}
        />
        <CardList year={year} week={week}/>
      </Grid>
    );
  }
}

export default withStyles(useStyles)(FrontPage);
