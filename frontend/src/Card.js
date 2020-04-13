import React from 'react';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import './Card.css'

export default function SimpleCard(props) {
  return (
    <Card elevation={2} className="card">
      <CardContent>
        <Typography color="textSecondary" gutterBottom>
          {props.rank}.
        </Typography>
        <Typography variant="h5" component="h2">
          {props.away} @ {props.home}
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small"><ExpandMoreIcon/> SPOILERS</Button>
      </CardActions>
    </Card>
  );
}
