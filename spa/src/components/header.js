import React from 'react';
import {
    Link
} from "react-router-dom";
import PropTypes from 'prop-types';

class Header extends React.Component {
  logged_out_nav () {
    return(
      <ul>
        <li><Link to="/app">login</Link></li>
        <li><Link to="/app/signup">signup</Link></li>
      </ul>
    );
  }

  logged_in_nav() {
    return (
      <ul>
        <li>Welcome, {this.props.user.first_name}</li>
        <li><Link to="/app/logout">logout</Link></li>
      </ul>
    );
  }

  render() {
    return (
      <div className="header">
        <nav>
          {this.props.user ? this.logged_in_nav() : this.logged_out_nav()}
        </nav>
      </div>
    );
  }
}
Header.propTypes = {
  user: PropTypes.object,
  set_page: PropTypes.func.isRequired,
  handle_logout: PropTypes.func.isRequired
};

export default Header;
