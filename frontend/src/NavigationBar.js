import React from 'react';
import 'typeface-roboto';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import './NavigationBar.css';

export default class NavigationBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      current: props.current,
    };
  }

  render() {
    return (
      <div className="root">
        <AppBar position="static" style={{ backgroundColor: '#084c61' }}>
        <Toolbar>
          <IconButton edge="start" className="menuButton" color="inherit" aria-label="menu">
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" className="navbartitle">
            {this.state.current}
          </Typography>
        </Toolbar>
      </AppBar>
      </div>
    );
  }
}
