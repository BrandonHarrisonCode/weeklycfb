import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Link from '@material-ui/core/Link';
import TabPanel from './TabPanel';

const useStyles = theme => ({
  title: {
    padding: '1em 5px 5px 1em',
    color: '#4f6d7a',
  },
}); 


class AboutPage extends TabPanel {
  render() {
    const classes = this.props.classes;

    if(this.props.currentTabName !== this.props.tabName) {
      return null;
    }
    return (
      <Grid
        container
        spacing={0}
        direction="column"
        alignItems="center"
        justify="center"
      >
        <Typography variant="h3" component="h1" className={classes.title}>About</Typography>
        <Typography variant="subtitle1" gutterBottom>
          Created by <Link href="https://github.com/BrandonHarrisonCode">Brandon Harrison</Link> and <Link href="https://github.com/andmcadams">Andrew McAdams</Link>
        </Typography>
        <Typography variant="body1" gutterBottom>
        </Typography>
      </Grid>
    );
  }
}

export default withStyles(useStyles)(AboutPage);
