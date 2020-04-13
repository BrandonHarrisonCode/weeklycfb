import React from 'react';
import 'typeface-roboto';
import Typography from '@material-ui/core/Typography';
import './FrontPage.css'
import CardList from './CardList';

export default class FrontPage extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <Typography variant="h3" className="title">CFB Game of the Week</Typography>
        <CardList />
      </div>
    );
  }
}
