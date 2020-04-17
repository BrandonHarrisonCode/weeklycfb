import React from 'react';
import './App.css';
import NavigationBar from './NavigationBar';
import FrontPage from './FrontPage'
import AboutPage from './AboutPage'

class App extends React.Component {
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
      <div>
        <NavigationBar 
          tabName={this.state.currentTabName} 
          handleTabChange={this.handleTabChange}
        />
        <FrontPage tabName="Home" currentTabName={this.state.currentTabName}/>
        <AboutPage tabName="About" currentTabName={this.state.currentTabName}/>
      </div>
    );
  }
}

export default App;
