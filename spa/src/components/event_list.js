import React from 'react';
import PropTypes from 'prop-types';

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
            <button
              onClick={() => this.props.set_page('event_detail', event.pk)}
            >
              {event.name}
            </button>
          </li>
        );
        elements.push(element);
      });
    }

    return elements;
  }

  componentDidMount() {
    fetch(`${this.props.api_host}/events/`, {
      headers: {
        Authorization: `JWT ${localStorage.getItem('token')}`
      }
    })
    .then(response => response.json())
    .then(blob => {
      this.setState({events: blob});
    })
    .catch(error => {
      console.log(error);
    });
  }

  render() {
    let create_button = null;
    if (this.props.is_logged_in) {
      create_button = this.make_create_button();
    }

    let event_elements = this.make_event_elements(this.state.events);

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
  is_logged_in: PropTypes.bool.isRequired,
  set_page: PropTypes.func.isRequired
};

export default EventList;
