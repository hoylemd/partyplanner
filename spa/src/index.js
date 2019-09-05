import React from 'react';
import ReactDOM from 'react-dom';

import Header from './components/header';
import LoginForm from './components/login_form';
import SignupForm from './components/signup_form';

import './index.css';

const API_HOST = 'http://localhost'

class PartyPlanner extends React.Component {
  handle_login = (e, data) => {
    e.preventDefault();

    fetch(`${API_HOST}/token-auth/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(blob => {
      localStorage.setItem('token', blob.token);
      this.setState({
        not_logged_in: false,
        displayed_form: '',
        user: blob.user
      });
    });
  };

  handle_signup = (e, data) => {
    e.preventDefault();

    fetch(`${API_HOST}/users/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(blob => {
      localStorage.setItem('token', blob.token);
      this.setState({
        not_logged_in: false,
        displayed_form: '',
        user: blob
      });
    });
  };

  handle_logout = () => {
    localStorage.removeItem('token');
    this.setState({
      not_logged_in: true,
      user: null
    });
  };

  /*
  set_form(form) {
    this.setState({
      displayed_form: form
    });
  }
  */

  set_form = form => {
    this.setState({
      displayed_form: form
    });
  };

  make_login_form = () => {
    return (
      <LoginForm handle_login={this.handle_login} />
    );
  };

  make_signup_form = () => {
    return (
      <SignupForm handle_signup={this.handle_signup} />
    );
  };

  get_form(name) {
    let maker = {
      'login': this.make_login_form,
      'signup': this.make_signup_form
    }[name];

    if (maker) return maker();
    return null;
  }

  componentDidMount() {
    if (this.state.not_logged_in) {
      return;
    }

    fetch(`${API_HOST}/whoami/`, {
      headers: {
        Authorization: `JWT ${localStorage.getItem('token')}`
      }
    })
    .then(response => response.json())
    .then(blob => {
      this.setState({ user: blob });
    });
  }

  render() {
    let form = this.get_form(this.state.displayed_form);

    return (
      <div className="partyPlanner">
        <Header
          user={this.state.user}
          set_form={this.set_form}
          handle_logout={this.handle_logout}
        />
        {form}
      </div>
    );
  }

  constructor(props) {
    super(props);
    this.state = {
      displayed_form: '',
      not_logged_in: localStorage.getItem('token') ? false : true,
      user: null
    };
  }
}

ReactDOM.render(
  <PartyPlanner />,
  document.getElementById('root')
);
