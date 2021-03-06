import React from 'react';
import ReactDOM from 'react-dom';
import {
    BrowserRouter as Router,
    Switch,
    Route,
} from "react-router-dom";

import Header from './components/header';
import LoginForm from './components/login_form';
import Logout from './components/logout';
import SignupForm from './components/signup_form';
import EventList from './components/event_list';
import EventDetail from './components/event_detail';

import './index.css';

const API_HOST = 'http://localhost/api'

class PartyPlanner extends React.Component {
  handle_login = (_data, blob, _response) => {
    localStorage.setItem('token', blob.token);
    return this.setState({
      not_logged_in: false,
      user: blob.user
    });
  };

  handle_signup = async (data, blob, response) => {
    localStorage.setItem('token', blob.token);
    return this.setState({
      not_logged_in: false,
      user: blob
    });
  };

  handle_logout = () => {
    localStorage.removeItem('token');
    this.setState({
      not_logged_in: true,
      user: null,
    });
  };

  set_page = (form, pk) => {
    pk = pk || null;
    this.setState({
      pk: pk
    });
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
    }[name] || this.make_login_form

    return maker(pk);
  }

  async componentDidMount() {
    if (this.state.not_logged_in) {
      return;
    }

    const url = `${API_HOST}/whoami/`;
    const headers = {
      Authorization: `JWT ${localStorage.getItem('token')}`
    };

    const response = await fetch(url, {headers: headers});

    if (response.ok) {
      const blob = await response.json();
      return this.setState({ user: blob });
    }
    if (response.status === 401) {
      return this.setState({goto: '/app'});
    }

    const message = `Error ${response.status}`;
    console.log(message);
    const blob = await response.json();
    console.log(blob);

    throw Error(message);
  }

  render() {
    return (
      <Router className="partyPlanner">
        <Header
          user={this.state.user}
          set_page={this.set_page}
          handle_logout={this.handle_logout}
        />
        <Switch>
          <Route exact path="/app/events">
            <EventList
              api_host={API_HOST}
              not_logged_in={this.state.not_logged_in}
              set_page={this.set_page}
            />
          </Route>
          <Route
            path="/app/events/:id"
            render={(props) => (
              <EventDetail
                pk={props.match.params.id}
                api_host={API_HOST}
              />
            )}
          />
          <Route path="/app/signup">
            <SignupForm
              handle_success={this.handle_signup}
              endpoint={`${API_HOST}/users/`}
              submit_label='Sign up'
              user={this.state.user}
            />
          </Route>
          <Route path="/app/logout">
            <Logout handle_logout={this.handle_logout} />
          </Route>
          <Route path="/app">
            <LoginForm
              handle_success={this.handle_login}
              endpoint={`${API_HOST}/token-auth/`}
              submit_label='Log in'
              user={this.state.user}
            />
          </Route>
          <Route>
            not found :c
          </Route>
        </Switch>
      </Router>
    );
  }

  constructor(props) {
    super(props);
    this.state = {
      not_logged_in: localStorage.getItem('token') ? false : true,
      error: null,
      user: null,
      goto: null,
    };
  }
}

ReactDOM.render(
  <PartyPlanner />,
  document.getElementById('root')
);
