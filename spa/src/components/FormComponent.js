import React from 'react';
import PropTypes from 'prop-types';

class FormComponent extends React.Component {
  fields = this.fields || {};  // populate this in extensions!

  /* e.g. field config
  fields = {
    name: {type: 'text', label: 'Name'},
    starts_at: {type: 'date', label: 'Starts at'}
  }
  */

  handle_change = (e) => {
    /* Extract the changed field from the dom and store in state */
    const field_name = e.target.name;
    const value = e.target.value;

    let new_state = {};
    new_state[field_name] = value;
    this.setState(new_state);
  };

  handle_submit = async (e, data) => {
    /* submit the form via AJAX */
    e.preventDefault();

    this.setState({errors: null, field_errors: {}});

    const response = await fetch(`${this.props.endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });


    if (response.ok) {
      const blob = await response.json();
      return this.props.handle_success(data, blob, response);
    }

    return this.handle_failure(data, response);
  };

  handle_failure = async (data, response) => {
    const blob = await response.json();
    let new_state = {...this.state};

    let field = '';
    for (field of Object.keys(blob)) {
      new_state.field_errors[field] = blob[field];
    }

    new_state.errors = 'Oepsie Woepsie! sumting went fucky-wucky!';
    this.setState(new_state);
  }

  makeField = (name, spec) => {
    let error = '';
    if (this.state.field_errors[name]) {
      error = (
        <span className={`error ${name}`}>
          {this.state.field_errors[name]}
        </span>
      )
    }

    return (
      <div className={`form-field ${name}`}>
        <label htmlFor={name}>{spec.label}</label>
        <input type={spec.type} name={name} value={this.state[name] || ''}
          onChange={this.handle_change} />
          {error}
      </div>
    )
  }

  makeFields = () => {
    let fields = [];
    let field = '';

    for (field of Object.keys(this.fields)) {
      let spec = this.fields[field];
      fields.push(this.makeField(field, spec));
    }

    return fields;
  };

  render() {
    let errors = '';

    if (this.state.errors) {
      errors = (
        <div className="error">
          {this.state.errors}
        </div>
      )
    }

    return (
      <form onSubmit={e => this.handle_submit(e, this.state)}>
        {this.makeFields()}
        {errors}
        <input type="submit" value={this.props.submit_label || 'Submit'}/>
      </form>
    );
  }

  constructor(props) {
    super(props);

    // config state
    this.state = this.state || {};

    this.state.field_errors = {};
    let field = '';
    for (field of Object.keys(this.fields)) {
      // pre-load from object, if passed
      if (props.object && props.object[field]) {
        this.state[field] = props.object[field];
      } else {
        this.state[field] = null;
      }
      this.state.field_errors[field] = null;
    }
  }
}

FormComponent.propTypes = {
  handle_success: PropTypes.func,
  endpoint: PropTypes.string.isRequired,
  object: PropTypes.object,
  submit_label: PropTypes.string
};

export default FormComponent;
