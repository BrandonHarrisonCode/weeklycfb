import React from 'react';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Grid from '@material-ui/core/Grid';
import Avatar from '@material-ui/core/Avatar';
import Typography from '@material-ui/core/Typography';
import './Card.css'

export default function SimpleCard(props) {
  return (
    <Card elevation={2} className="card">
      <CardContent>
        <Typography color="textSecondary" gutterBottom>
          {props.rank === 1 ? props.rank + ". Top game of the week." : props.rank + "."}
        </Typography>
        <Grid
          container
          direction="column"
          justify="flex-start"
        >
          <Grid 
            container
            item
            direction="row"
            justify="flex-start"
            alignItems="center"
            xs={12}
          >
            <Grid item sm={1} xs={2}>
              <Avatar alt={props.away} src={"https://weeklycfb-team-logos.s3.amazonaws.com/" + encodeURI(props.away) + ".png"} />
            </Grid>
            <Grid item sm={11} xs={10}>
              <Typography variant="h5" component="h2">
                {props.away}
              </Typography>
            </Grid>
          </Grid>
          <Grid 
            container
            item
            direction="row"
            justify="flex-start"
            alignItems="center"
            xs={12}
          >
            <Grid item sm={1} xs={2}>
              <Avatar alt={props.home} src={"https://weeklycfb-team-logos.s3.amazonaws.com/" + encodeURI(props.home) + ".png"} />
            </Grid>
            <Grid item sm={11} xs={10}>
              <Typography variant="h5" component="h2">
                {props.home}
              </Typography>
            </Grid>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}
