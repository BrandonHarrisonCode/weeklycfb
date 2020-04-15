import React from 'react';
import 'typeface-roboto';
import Paper from '@material-ui/core/Paper';
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
 
    this.fetchGames();
  }

  async componentDidUpdate(prevProps) {
    if(prevProps.year !== this.props.year || prevProps.week !== this.props.week) {
      this.fetchGames();
    }
  }

  async fetchGames() {
    const url = 'https://api.cfbgameoftheweek.com/entertainmentScores?week=' + this.props.week + '&year=' + this.props.year;
    const response = await fetch(url);
    const parsedJSON = await response.json();

    this.setState({
      gamesData: parsedJSON.data, 
      loading: false
    });
  }

  render() {
    const {loading, gamesData} = this.state;
    return (
      <Paper elevation={3} className="cardList">
        <List>
          {
            loading ? "loading..." : 
              gamesData.slice(0,10).map((game, rank) => {
                const {home, away} = game;
                return (
                  <ListItem key={rank}>
                    <Card rank={rank+1} home={home} away={away}/>
                  </ListItem>
                )})
          }
        </List>
      </Paper>
    );
  }
}
