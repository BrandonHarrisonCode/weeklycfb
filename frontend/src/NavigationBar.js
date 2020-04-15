import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import 'typeface-roboto';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import WeekSelector from './WeekSelector'

const useStyles = theme => ({
  root: {
    flexGrow: 1,
  },
  pageTabs: {
    flexGrow: 1,
  }
}); 

class NavigationBar extends React.Component {
  constructor(props) {
    super(props);
    this.handleYearChange = this.handleYearChange.bind(this);
    this.handleWeekChange = this.handleWeekChange.bind(this);

    this.state = {
      current: props.current,
      anchorEl: null,
    };
  }

  handleYearChange(value) {
    this.props.handleYearChange(value);
  }

  handleWeekChange(value) {
    this.props.handleWeekChange(value);
  }

  handlePageChange(event, newValue) {
    console.log(newValue);
    this.setState({
      current: newValue,
    });
  }

  render() {
    const classes = this.props.classes;
    return (
      <div className={classes.root}>
        <AppBar position="static" style={{ backgroundColor: '#084c61' }}>
          <Toolbar>
            <Tabs value={this.state.current} onChange={this.handlePageChange.bind(this)} aria-label="page navigation" className={classes.pageTabs}>
              <Tab label="Home" />
              <Tab label="About" />
            </Tabs>
            <WeekSelector 
              year={this.props.year}
              week={this.props.week}
              handleYearChange={this.handleYearChange} 
              handleWeekChange={this.handleWeekChange}
            />
          </Toolbar>
        </AppBar>
      </div>
    );
  }
}

export default withStyles(useStyles)(NavigationBar);
