import React from 'react';
import ReactDOM from 'react-dom';
import FrontPage from './FrontPage';

describe("FrontPage", () => {
  it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<FrontPage tabName="Home" currentTabName="Home"/>, div);
    ReactDOM.unmountComponentAtNode(div);
  });
});
