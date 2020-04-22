import React from 'react';
import ReactDOM from 'react-dom';
import AboutPage from './AboutPage';

describe("AboutPage", () => {
  it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<AboutPage tabName="About" currentTabName="About"/>, div);
    ReactDOM.unmountComponentAtNode(div);
  });
});
