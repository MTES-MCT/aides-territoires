import React from "react";
import { withRouter } from "react-router";
import { graphql } from "react-apollo";
import gql from "graphql-tag";
import { SubmissionError } from "redux-form";
import { compose } from "react-apollo";
import { setToken } from "../../lib/auth";
import apolloClient from "../../lib/apolloClient";

/**
 * Logs user to the serveur from a LoginForm returning
 * a password and
 * @param {React.Component} LoginForm
 */
export default function withLoginToServer(LoginForm) {
  class LoginFormContainer extends React.Component {
    constructor(props) {
      super(props);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
    handleSubmit = async ({ password, email }) => {
      const { login, history } = this.props;
      try {
        const {
          data: {
            login: { jwt }
          }
        } = await login({ variables: { password, email } });
        setToken(jwt);
        await apolloClient.resetStore();
        history.push("/admin");
      } catch (err) {
        throw new SubmissionError({
          _err: "Login error"
        });
      }
    };

    componentDidMount() {
      //this.timeout = setInterval(this.props.data.refetch, 1000);
    }

    componentWillUnmount() {
      //clearInterval(this.timeout);
    }

    render() {
      return <LoginForm onSubmit={this.handleSubmit} />;
    }
  }

  const query = gql`
    mutation login($email: String!, $password: String!) {
      login(email: $email, password: $password) {
        jwt
        user {
          id
        }
      }
    }
  `;

  return compose(
    withRouter,
    graphql(query, { name: "login" })
  )(LoginFormContainer);
}
