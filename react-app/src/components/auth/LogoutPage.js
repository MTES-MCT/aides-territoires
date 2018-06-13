import React from "react";
import { compose } from "react-apollo";
import { withRouter } from "react-router";
import { setToken } from "../../lib/auth";
import apolloClient from "../../lib/apolloClient";

class Logout extends React.Component {
  async componentDidMount() {
    setToken(null);
    await apolloClient.resetStore();
    this.props.history.push("/");
  }

  render() {
    return null;
  }
}

export default compose(withRouter)(Logout);
