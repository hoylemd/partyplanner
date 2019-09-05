import React from 'react';
import PropTypes from 'prop-types';

class EventDetail extends React.Component {
  make_event_details(event) {
    let image = null;
    if (event.image) {
      image = (
        <img src={event.image} title={event.name + ' picture'}/>
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

    debugger;
    return (
      <>
      <h1>{event.name}</h1>
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

  componentDidMount() {
    fetch(`${this.props.api_host}/events/${this.props.pk}`, {
      headers: {
        Authorization: `JWT ${localStorage.getItem('token')}`
      }
    })
    .then(response => response.json())
    .then(blob => {
      this.setState({event: blob});
    });
  }

  render () {
    let event_details = (
      <span>Loading...</span>
    );

    if (this.state.event) {
      event_details = this.make_event_details(this.state.event);
    }

    return (
      <div className="event_detail">
        <button onClick={() => this.props.set_page('event_list')}>
          Back to List
        </button>
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
