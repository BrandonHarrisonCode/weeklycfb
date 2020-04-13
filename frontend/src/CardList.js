import React from 'react';
import Card from './Card'

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
 
    const url = 'https://feqt8qhih9.execute-api.us-east-1.amazonaws.com/Production/entertainmentScores?week=1&year=2019'
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
      <div>
        {
          loading ? "loading..." : 
              gamesData.map((game, rank) => {
                const {home, away} = game;
                return (
                  <li key={rank}>
                    <Card rank={rank+1} home={home} away={away}/>
                  </li>
                )})
        }
      </div>
      //<Card rank="1" home="Utah State" away="Wake Forest"/>
    );
  }
}
