import React from 'react';
import PropTypes from 'prop-types';

class Header extends React.Component {
  logged_out_nav () {
    return(
      <ul>
        <li onClick={() => this.props.set_page('login')}>login</li>
        <li onClick={() => this.props.set_page('signup')}>signup</li>
      </ul>
    );
  }

  logged_in_nav() {
    return (
      <ul>
        <li>Welcome, {this.props.user.first_name}</li>
        <li onClick={this.props.handle_logout}>logout</li>
      </ul>
    );
  }

  render() {
    return (
      <div className="header">
        {this.props.user ? this.logged_in_nav() : this.logged_out_nav()}
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
