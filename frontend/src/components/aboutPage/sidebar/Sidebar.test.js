import React from 'react';
import ReactDOM from 'react-dom';

import GitHubIcon from '@material-ui/icons/GitHub';

import Sidebar from './Sidebar';

describe("Sidebar", () => {
  let title = 'About Us';
  let description = 'This project was created by Brandon Harrison and Andrew McAdams.';
  let social = [
    { name: 'GitHub', icon: GitHubIcon, url: 'https://github.com/BrandonHarrisonCode/weeklycfb' },
  ];


  it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(
      <Sidebar 
        title={title}
        description={description}
        social={social}
      />, div);
    ReactDOM.unmountComponentAtNode(div);
  });
});
