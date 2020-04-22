import React from 'react';
import ReactDOM from 'react-dom';
import WeeklyCFB from './WeeklyCFB';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<WeeklyCFB />, div);
  ReactDOM.unmountComponentAtNode(div);
});
