import React from "react";
import { withRouter } from "react-router";
import { graphql } from "react-apollo";
import gql from "graphql-tag";
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
    state = {
      graphQLErrors: null
    };
    handleSubmit = async ({ password, email }) => {
      const { login, history } = this.props;
      try {
        const result = await login({ variables: { password, email } });
        setToken(result.data.login.jwt);
        await apolloClient.resetStore();
        history.push("/admin");
      } catch (error) {
        this.setState({
          errors: error.graphQLErrors
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
      return (
        <div>
          {this.state.errors && <LoginErrors errors={this.state.errors} />}
          <LoginForm onSubmit={this.handleSubmit} />
        </div>
      );
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

const LoginErrors = ({ errors }) => {
  return (
    <div className="message is-danger">
      <div className="message-body">
        {errors.map(error => {
          return <p key={error.message}>{error.message}</p>;
        })}
      </div>
    </div>
  );
};
