import React from 'react';
import 'typeface-roboto';
import Typography from '@material-ui/core/Typography';
import './FrontPage.css'
import NavigationBar from './NavigationBar';
import CardList from './CardList';

export default class FrontPage extends React.Component {
  render() {
    return (
      <div>
        <NavigationBar current={0} />
        <Typography variant="h3" component="h1" className="title">CFB Game of the Week</Typography>
        <CardList />
      </div>
    );
  }
}
