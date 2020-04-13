import React from 'react';
import 'typeface-roboto';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import './CardList.css';
import Card from './Card';

export default class CardList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      gamesData: [],
    };
  }

  async componentDidMount() {
    this.setState({
      gamesData: [], 
      loading: true
    });
 
    const url = 'https://api.cfbgameoftheweek.com/entertainmentScores?week=1&year=2019'
    const response = await fetch(url);
    const parsedJSON = await response.json();

    this.setState({
      gamesData: parsedJSON.data, 
      loading: false
    });
    console.log(parsedJSON.data);
    console.log(parsedJSON.data.length);
  }

        //{this.state.loading ? <div>loading...</div> : <div>this.state.gamesData.map((game, rank) => <Card rank={rank} home="{game.home}" away="{game.away}"/>);</div>}
  render() {
    const {loading, gamesData} = this.state;
    return (
      <Paper elevation={3} className="cardList">
        <Typography variant="h3" gutterBottom> CFB Game of the Week </Typography>
        <List>
          {
            loading ? "loading..." : 
              gamesData.slice(0,10).map((game, rank) => {
                const {home, away} = game;
                return (
                  <ListItem>
                    <Card rank={rank+1} home={home} away={away}/>
                  </ListItem>
                )})
          }
        </List>
      </Paper>
      //<Card rank="1" home="Utah State" away="Wake Forest"/>
    );
  }
}
