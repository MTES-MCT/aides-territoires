import React from "react";
import { compose } from "react-apollo";
import { withRouter } from "react-router";
import LoginForm from "./LoginForm";
import Layout from "../layouts/Layout";

class LoginPage extends React.Component {
  render() {
    return (
      <Layout>
        <section className="section">
          <div className="container">
            <LoginForm />
          </div>
        </section>
      </Layout>
    );
  }
}

export default LoginPage;
