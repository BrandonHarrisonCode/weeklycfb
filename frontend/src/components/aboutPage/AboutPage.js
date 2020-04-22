import React from 'react';
import { withStyles } from '@material-ui/core/styles';

import GitHubIcon from '@material-ui/icons/GitHub';

import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import Divider from '@material-ui/core/Divider';
import Typography from '@material-ui/core/Typography';

import TabPanel from '../common/TabPanel';
import Sidebar from './sidebar';

import Markdown from '../common/Markdown';
import aboutPageContent from './markdown/About.md';
import detailedContent from './markdown/AboutDetailed.md';

const useStyles = theme => ({
  markdown: {
    ...theme.typography.body1,
    padding: theme.spacing(3, 0),
  },
   markdownDetailed: {
    ...theme.typography.body2,
    padding: theme.spacing(3, 0),
  },
  title: {
    color: '#4f6d7a',
  },
  mainGrid: {
    marginTop: theme.spacing(5),
  },
}); 

const sidebar = {
  title: 'About Us',
  description:
    'This project was created by Brandon Harrison with help from Andrew McAdams for the initial portion of the project.',
  social: [
    { name: 'GitHub', icon: GitHubIcon, url: 'https://github.com/BrandonHarrisonCode/weeklycfb' },
  ],
};

class AboutPage extends TabPanel {
  constructor(props) {
    super(props)

    this.state = {
      content: "",
      detailedContent: "",
    };
  }

  componentDidMount() {
    fetch(aboutPageContent).then((response) => response.text()).then((text) => {
      this.setState({ content: text })
    })
    fetch(detailedContent).then((response) => response.text()).then((text) => {
      this.setState({ detailedContent: text })
    })
  }

  render() {
    const classes = this.props.classes;
    const content = this.state.content;
    const detailedContent = this.state.detailedContent;

    if(this.props.currentTabName !== this.props.tabName) {
      return null;
    }
    return (
      <Container maxWidth="lg">
        <Grid container spacing={4} className={classes.mainGrid}>
          <Grid item xs={12} md={8}>
            <Typography variant="h3" component="h1" className={classes.title}>
              About the Site
            </Typography>
            <Divider />
            <Markdown className={classes.markdown}>
              {content}
            </Markdown>
            <Divider />
            <Markdown className={classes.markdownDetailed}>
              {detailedContent}
            </Markdown>
          </Grid>
          <Sidebar
            title={sidebar.title}
            description={sidebar.description}
            social={sidebar.social}
          />
        </Grid>
      </Container>
    );
  }
}

export default withStyles(useStyles)(AboutPage);
