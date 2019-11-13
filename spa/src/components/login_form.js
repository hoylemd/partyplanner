import React from 'react';
import PropTypes from 'prop-types';
import { Redirect } from 'react-router-dom';

class LoginForm extends React.Component {
  handle_change = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    this.setState(prevstate => {
      const newState = { ...prevstate };
      newState[name] = value;
      return newState;
    });
  };

  handle_submit = async (e, data) => {
    e.preventDefault();

    const response = await fetch(`${this.props.api_host}/token-auth/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })

    if (response.ok) {
      const blob = await response.json();
      return this.props.handle_login(blob.token, blob.user);
    }

    return this.setState({
      login_failed: true
    });
  };

  render() {
    if (this.props.user) {
      return (
        <Redirect to="/app/events"/>
      )
    }

    let error_display = '';
    if (this.state.login_failed) {
      error_display = (
        <div className="error">
          Sorry, login failed. Check your credentials and try again.
        </div>
      );
    }

    return (
      <form onSubmit={e => this.handle_submit(e, this.state)}>
        <div>
          <h4>Log In</h4>
          <label htmlFor="username">Username</label>
          <input
            type="text"
            name="username"
            value={this.state.username}
            onChange={this.handle_change}
          />
          <label htmlFor="password">Password</label>
          <input
            type="password"
            name="password"
            value={this.state.password}
            onChange={this.handle_change}
          />
        </div>
        {error_display}
        <input type="submit" value="Log in"/>
      </form>
    );
  }

  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      login_failed: false
    };
  }
}
LoginForm.propTypes = {
  handle_login: PropTypes.func.isRequired,
  user: PropTypes.object,
  api_host: PropTypes.string
};

export default LoginForm;
