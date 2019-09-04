import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

class ppHeader extends React.Component {
  render() {
    return (
      <div className="header">
        Login
      </div>
    )
  }

  constructor(props) {
    super(props);

    this.state = {

    };
  }
}
ppHeader.propTypes = {

};

class PartyPlanner extends React.Component {

  render() {
    return (
      <div className="partyPlanner">
        <ppHeader />
        <p>Hello, World!</p>
      </div>
    );
  }

  constructor(props) {
    super(props);
    this.state = {
    };
  }
}

ReactDOM.render(
  <PartyPlanner />,
  document.getElementById('root')
);
