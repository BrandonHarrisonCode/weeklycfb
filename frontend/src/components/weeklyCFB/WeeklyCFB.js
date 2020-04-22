import React from 'react';
import './WeeklyCFB.css';
import NavigationBar from '../navBar/';
import FrontPage from '../frontPage/'
import AboutPage from '../aboutPage/'

class WeeklyCFB extends React.Component {
  constructor(props) {
    super(props);
    this.handleTabChange = this.handleTabChange.bind(this);

    this.state = {
      currentTabName: 'Home',
    }
  }

  handleTabChange(value) {
    this.setState({currentTabName: value});
  }

  render() {
    return (
      <React.Fragment>
        <NavigationBar 
          tabName={this.state.currentTabName} 
          handleTabChange={this.handleTabChange}
        />
        <FrontPage tabName="Home" currentTabName={this.state.currentTabName}/>
        <AboutPage tabName="About" currentTabName={this.state.currentTabName}/>
      </React.Fragment>
    );
  }
}

export default WeeklyCFB;
