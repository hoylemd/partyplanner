import React from 'react';
import PropTypes from 'prop-types';
import { Redirect } from 'react-router-dom';

import FormComponent from './FormComponent';

class SignupForm extends FormComponent {
  fields = {
    username: {type: 'text', label: 'Username'},
    first_name: {type: 'text', label: 'First name'},
    last_name: {type: 'text', label: 'Last name'},
    email: {type: 'email', label: 'Email address'},
    password: {type: 'password', label: 'Password'}
  };

  render() {
    // Redirect to event list if logged in
    if (this.props.user) {
      return <Redirect to="/app/events"/>
    }

    return (
      <>
        <h4>Sign up</h4>
        {super.render()}
      </>
    );
  }
}
SignupForm.propTypes = {
  ...FormComponent.propTypes,
  user: PropTypes.object,
};
export default SignupForm;
