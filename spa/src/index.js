import React from 'react';
import ReactDOM from 'react-dom';

import Header from './components/header';
import LoginForm from './components/login_form';
import SignupForm from './components/signup_form';
import EventList from './components/event_list';
import EventDetail from './components/event_detail';

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
        displayed_page: '',
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
        displayed_page: '',
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

  set_page = (form, pk) => {
    pk = pk || null;
    this.setState({
      displayed_page: form,
      pk: pk
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

  make_event_list = () => {
    return (
      <EventList
        api_host={API_HOST}
        is_logged_in={!this.state.not_logged_in}
        set_page={this.set_page}
      />
    );
  };

  make_event_form = () => {
    return (
      <div>Event form</div>
    );
  };

  make_event_detail = (pk) => {
    return (
      <EventDetail
        api_host={API_HOST}
        set_page={this.set_page}
        pk={pk}
      />
    )
  };

  get_page(name, pk) {
    pk = pk || null;
    let maker = {
      'login': this.make_login_form,
      'signup': this.make_signup_form,
      'event_list': this.make_event_list,
      'event_create': this.make_event_form,
      'event_detail': this.make_event_detail,
    }[name] || this.make_event_list

    return maker(pk);
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
    let page = this.get_page(this.state.displayed_page, this.state.pk);

    return (
      <div className="partyPlanner">
        <Header
          user={this.state.user}
          set_page={this.set_page}
          handle_logout={this.handle_logout}
        />
        {page}
      </div>
    );
  }

  constructor(props) {
    super(props);
    this.state = {
      displayed_page: '',
      not_logged_in: localStorage.getItem('token') ? false : true,
      user: null
    };
  }
}

ReactDOM.render(
  <PartyPlanner />,
  document.getElementById('root')
);
