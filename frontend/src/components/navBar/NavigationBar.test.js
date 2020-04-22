import React from 'react';
import ReactDOM from 'react-dom';
import NavigationBar from './NavigationBar';

describe("NaviagtionBar", () => {
  let wrapper;
  let mockTabChange;

  beforeEach(() => {
    mockTabChange = jest.fn();
  });

  it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<NavigationBar tabName="Home" handleTabChange={mockTabChange}/>, div);
    ReactDOM.unmountComponentAtNode(div);
  });
});
