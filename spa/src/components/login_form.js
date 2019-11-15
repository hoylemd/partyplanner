import React from 'react';
import PropTypes from 'prop-types';
import { Redirect } from 'react-router-dom';

import FormComponent from './FormComponent';

class LoginForm extends FormComponent {
  fields = {
    username: {type: 'text', label: 'Username'},
    password: {type: 'password', label: 'Password'}
  };

  render() {
    // Redirect to event list if logged in
    if (this.props.user) {
      return <Redirect to="/app/events"/>
    }

    return (
      <>
        <h4>Log In</h4>
        {super.render()}
      </>
    );
  }
}
LoginForm.propTypes = {
  ...FormComponent.propTypes,
  user: PropTypes.object,
};

export default LoginForm;
