import React from 'react';
import './WeeklyCFB.css';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import 'typeface-cabin'
import NavigationBar from '../navBar/';
import FrontPage from '../frontPage/'
import AboutPage from '../aboutPage/'

const theme = createMuiTheme({
  typography: {
    fontFamily: 'Cabin, sans-serif',
  },
});

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
      <ThemeProvider theme={theme}>
        <NavigationBar 
          tabName={this.state.currentTabName} 
          handleTabChange={this.handleTabChange}
        />
        <FrontPage tabName="Home" currentTabName={this.state.currentTabName}/>
        <AboutPage tabName="About" currentTabName={this.state.currentTabName}/>
      </ThemeProvider>
    );
  }
}

export default WeeklyCFB;
