import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

class EventDetail extends React.Component {
  make_event_details(event) {
    let image = null;
    if (event.image) {
      image = (
        <img src={event.image} alt={event.name + ' picture'}/>
      );
    }

    let register_button = (
      <button>Register for this Event</button>
    );
    let guest_list = (
      <ul>
        <li>Nobody yet!</li>
      </ul>
    );

    return (
      <>
      <h1>{event.name}</h1>
      {image}
      <h3>Hosted by {event.owner}</h3>
      <p>{event.description}</p>
      <div>
        <strong>Starts @:</strong> <span>{event.starts_at}</span>
      </div>
      <div>
        <strong>Ends @:</strong> <span>{event.ends_at}</span>
      </div>

      <h3>Guest List:</h3>
      {register_button}

      {guest_list}
      </>
    );
  }

  async componentDidMount() {
    const url = `${this.props.api_host}/events/${this.props.pk}`;
    const headers = {
      Authorization: `JWT ${localStorage.getItem('token')}`
    };
    const response = await fetch(url, {headers: headers});
    if (response.ok) {
      const blob = await response.json();
      return this.setState({event: blob});
    }
    if (response.status === 401) {
      return this.setState({goto: '/app'});
    }
    if (response.status === 404) {
      this.setState({notFound: true});
      throw Error(`event ${this.props.pk} not found`);
    }

    const message = `Error ${response.status}`;
    console.log(message);
    const blob = await response.json();
    console.log(blob);

    throw Error(message);
  }

  render () {
    let event_details = (
      <span>Loading...</span>
    );

    if (this.state.event) {
      event_details = this.make_event_details(this.state.event);
    } else if (this.state.notFound) {
      event_details = (
        <div className="not_found">
          Sorry, Event with id '{this.props.pk}' was not found.
        </div>
      )
    }

    return (
      <div className="event_detail">
        <Link to="/app/events">
          Back to List
        </Link>
        <div className="event">
          {event_details}
        </div>
      </div>
    );
  }

  constructor(props) {
    super(props);
    this.state = {
      event: null
    };
  }
}
EventDetail.propTypes = {
  api_host: PropTypes.string.isRequired,
  pk: PropTypes.number.isRequired,
  set_page: PropTypes.func.isRequired
};

export default EventDetail;
