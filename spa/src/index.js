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
  handle_login = async (e, data) => {
    e.preventDefault();

    const response = await fetch(`${API_HOST}/token-auth/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    const blob = await response.json()
    localStorage.setItem('token', blob.token);
    this.setState({
      not_logged_in: false,
      user: blob.user
    });
  };

  handle_signup = async (e, data) => {
    e.preventDefault();

    const response = await fetch(`${API_HOST}/users/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    const blob = await response.json()
    localStorage.setItem('token', blob.token);
    this.setState({
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

    const url = `${this.props.api_host}/whoami`;
    const headers = {
      Authorization: `JWT ${localStorage.getItem('token')}`
    };

    const response = await fetch(url, {headers: headers});

    if (response.ok) {
      const blob = await response.json();
      return this.setState({ user: blob });
    }
    if (response.status == 401) {
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
          <Route path="/app/signup">
            <SignupForm handle_signup={this.handle_signup} />
          </Route>
          <Route exact path="/app/events">
            event list
            <EventList
              api_host={API_HOST}
              is_logged_in={!this.state.not_logged_in}
              set_page={this.set_page}
            />
          </Route>
          <Route
            path="/app/events/:id"
            render={
              (props) => <EventDetail
                          pk={props.match.params.id}
                          api_host={API_HOST}/>
            }
          />
          <Route path="/app/logout">
            <Logout handle_logout={this.handle_logout} />
          </Route>
          <Route path="/app">
            <LoginForm handle_login={this.handle_login} user={this.state.user}/>
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
      user: null
    };
  }
}

ReactDOM.render(
  <PartyPlanner />,
  document.getElementById('root')
);
