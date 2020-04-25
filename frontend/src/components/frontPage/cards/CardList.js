import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Snackbar from '@material-ui/core/Snackbar';
import Alert from '@material-ui/lab/Alert';
import Backdrop from '@material-ui/core/Backdrop';
import CircularProgress from '@material-ui/core/CircularProgress';
import Paper from '@material-ui/core/Paper';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import './CardList.css';
import Card from './Card';

const useStyles = theme => ({
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: '#fff',
  },
});

class CardList extends React.Component {
  constructor(props) {
    super(props);

    this.handleErrorClose = this.handleErrorClose.bind(this);

    this.state = {
      loading: true,
      gamesData: [],
      error: false,
    };
  }

  handleErrorClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    this.setState({
      error: false
    });
  }

  async componentDidMount() {
    this.setState({
      gamesData: [], 
      loading: true,
      error: false,
    });
 
    this.fetchGames();
  }

  async componentDidUpdate(prevProps) {
    if(prevProps.year !== this.props.year || prevProps.week !== this.props.week) {
      this.fetchGames();
    }
  }

  async fetchGames() {
    this.setState({
      loading: true
    });

    const url = 'https://api.cfbgameoftheweek.com/entertainmentScores?week=' + this.props.week + '&year=' + this.props.year;
    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Error while downloading data about the week.');
        }
        return response.json();
      })
      .then((parsedJSON) => {
        this.setState({
          gamesData: parsedJSON.data, 
          loading: false,
          error: false
        });
      })
    .catch((error) => {
      console.error('Unable to access the api at:', url);
      this.setState({
        loading: false,
        error: true
      });
    });
  }

  render() {
    const classes = this.props.classes;
    const {loading, gamesData, error} = this.state;

    return (
      <Paper elevation={3} className="cardList">
        <List>
          {
            loading ? 
              <Backdrop className={classes.backdrop} open={true}>
                <CircularProgress color="inherit" />
              </Backdrop>
            : error ?
              <Snackbar open={error} autoHideDuration={6000} onClose={this.handleErrorClose}> 
                <Alert severity="error" variant="filled" onClose={this.handleErrorClose}>
                  Error: Unable to access the data for this week!
                </Alert>
              </Snackbar>
              : gamesData.slice(0,10).map((game, rank) => {
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

export default withStyles(useStyles)(CardList);
