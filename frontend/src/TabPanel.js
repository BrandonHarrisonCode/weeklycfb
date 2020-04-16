import React from 'react';
import PropTypes from 'prop-types';

export default class TabPanel extends React.Component {
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
};
