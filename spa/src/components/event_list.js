import React from 'react';
import PropTypes from 'prop-types';

import {Link, Redirect} from 'react-router-dom';

class EventList extends React.Component {

  make_create_button() {
    return (
      <button onClick={() => this.props.set_page('new_event')}>
        Create new Event
      </button>
    );
  }

  make_event_elements(events) {
    let elements = [];

    if (events.forEach) {
      events.forEach(event => {
        let element = (
          <li key={event.pk}>
            <Link to={`/app/events/${event.pk}`}>
              {event.name}
            </Link>
          </li>
        );
        elements.push(element);
      });
    }

    return elements;
  }

  async get_events() {
    const url = `${this.props.api_host}/events/`;
    const headers = {
      Authorization: `JWT ${localStorage.getItem('token')}`
    };

    const response = await fetch(url, {headers: headers});

    if (response.ok) {
      const blob = await response.json();
      return this.setState({events: blob});
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

  async componentDidMount() {
    if (this.props.not_logged_in) {
      return this.setState({'goto': '/app'});
    }

    if (!this.state.events) {
      return await this.get_events();
    }
  }

  render() {
    // Handle nav directive
    if (this.state.goto) {
      return (
        <Redirect to={this.state.goto} />
      )
    }

    const create_button = this.make_create_button();

    const event_elements = this.make_event_elements(this.state.events);

    return (
      <div className="event_list">
        <h1>List of Events</h1>
        {create_button}

        <ul>
          {event_elements}
        </ul>
      </div>
    );
  }

  constructor(props) {
    super(props);
    this.state = {
      events: []
    };
  }
}
EventList.propTypes = {
  api_host: PropTypes.string.isRequired,
  not_logged_in: PropTypes.bool.isRequired,
  set_page: PropTypes.func.isRequired
};

export default EventList;
