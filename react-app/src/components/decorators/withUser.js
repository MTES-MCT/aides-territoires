import React from "react";
import { Redirect } from "react-router";
import { graphql } from "react-apollo";
import gql from "graphql-tag";
import hoistNonReactStatic from "hoist-non-react-statics";
import AppLoader from "../ui/AppLoader";
import GraphQLError from "../ui/GraphQLError";

const getDisplayName = WrappedComponent =>
  WrappedComponent.displayName || WrappedComponent.name || "Component";

export default function withUser(options = {}) {
  return WrappedComponent => {
    class WithUser extends React.Component {
      static displayName = `WithUser(${getDisplayName(WrappedComponent)})`;

      render() {
        const {
          data: { loading, error, user }
        } = this.props;

        if (loading) return <AppLoader />;
        if (error) return <GraphQLError error={error} />;

        if (options.mandatory && !user) return <Redirect to="/login" />;
        return <WrappedComponent {...this.props} user={user} />;
      }
    }

    WithUser = graphql(
      gql`
        query getUser {
          user {
            id
            email
            name
            roles
            permissions
          }
        }
      `,
      {
        options: {
          // notre composant peut être appelé de multiple fois, il vaut mieux
          // garder en cache le résultat.
          fetchPolicy: "cache-first"
        }
      }
    )(WithUser);

    hoistNonReactStatic(WithUser, WrappedComponent);

    return WithUser;
  };
}
