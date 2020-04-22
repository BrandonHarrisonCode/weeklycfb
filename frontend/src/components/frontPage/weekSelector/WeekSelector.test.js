import React from 'react';
import ReactDOM from 'react-dom';
import WeekSelector from './WeekSelector';

describe("WeekSelector", () => {
  let year;
  let week;
  let mockYearChange;
  let mockWeekChange;

  beforeEach(() => {
    year = "2019";
    week = "1";
    mockYearChange = jest.fn();
    mockWeekChange = jest.fn();
  });

  it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(
      <WeekSelector 
        year={year}
        week={week}
        handleYearChange={mockYearChange}
        handleWeekChange={mockWeekChange}
      />, div);
    ReactDOM.unmountComponentAtNode(div);
  });
});
