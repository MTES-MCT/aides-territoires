import React from "react";
import { withRouter } from "react-router";
import { graphql } from "react-apollo";
import gql from "graphql-tag";
import { reduxForm, Field, SubmissionError } from "redux-form";
import { compose } from "react-apollo";
import Layout from "../layouts/Layout";
import Text from "../ui/finalFormBulma/Text";
import ButtonSubmitWithLoader from "../ui/bulma/ButtonSubmitWithLoader";
import { setToken } from "../../lib/auth";
import apolloClient from "../../lib/apolloClient";

class LoginPage extends React.Component {
  handleSubmit = async values => {
    const { login, history } = this.props;

    try {
      const {
        data: {
          login: { jwt }
        }
      } = await login({ variables: values });

      setToken(jwt);

      await apolloClient.resetStore();

      history.push("/admin");
    } catch (err) {
      throw new SubmissionError({
        _err: "NONONONONONO"
      });
    }
  };

  render() {
    const { handleSubmit, submitting } = this.props;

    return (
      <Layout className="LoginPage">
        <section className="section">
          <div className="container">
            <section className="section">
              <form onSubmit={handleSubmit(this.handleSubmit)}>
                <Field className="is-large" name="email" component={Text} />
                <Field
                  className="is-large"
                  name="password"
                  component={Text}
                  type="password"
                />

                <ButtonSubmitWithLoader
                  className="button is-large is-info"
                  type="submit"
                  isLoading={submitting}
                >
                  Se connecter
                </ButtonSubmitWithLoader>
              </form>
            </section>
          </div>
        </section>
      </Layout>
    );
  }
}

export default compose(
  withRouter,
  reduxForm({
    form: "login",
    initialValues: {
      email: "yannb@protonmail.com",
      password: "hello"
    }
  }),
  graphql(
    gql`
      mutation login($email: String!, $password: String!) {
        login(email: $email, password: $password) {
          jwt
          user {
            id
          }
        }
      }
    `,
    {
      name: "login"
    }
  )
)(LoginPage);
