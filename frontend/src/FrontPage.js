import React from 'react';
import 'typeface-roboto';
import Typography from '@material-ui/core/Typography';
import './FrontPage.css'
import NavigationBar from './NavigationBar';
import CardList from './CardList';

export default class FrontPage extends React.Component {
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
    const year = this.state.year;
    const week = this.state.week;

    return (
      <div>
        <NavigationBar 
          current={0} 
          year={this.state.year}
          week={this.state.week}
          handleYearChange={this.handleYearChange} 
          handleWeekChange={this.handleWeekChange}
        />
        <Typography variant="h3" component="h1" className="title">CFB Game of the Week</Typography>
        <CardList year={year} week={week}/>
      </div>
    );
  }
}
