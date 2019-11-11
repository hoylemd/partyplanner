import React from 'react';
import PropTypes from 'prop-types';
import { Redirect } from 'react-router-dom';

class Logout extends React.Component {
  render() {
    this.props.handle_logout();

    return (
      <Redirect to="/"/>
    );
  }
}
Logout.propTypes = {
  handle_logout: PropTypes.func.isRequired
}

export default Logout;
