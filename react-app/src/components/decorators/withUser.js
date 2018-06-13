import React from "react";
import { Redirect } from "react-router";
import { graphql } from "react-apollo";
import gql from "graphql-tag";
import hoistNonReactStatic from "hoist-non-react-statics";

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

        if (loading) return "Loading...";
        if (error) return <GraphQLError error={error} />;

        if (options.mandatory && !user) return <Redirect to="/login" />;

        return <WrappedComponent {...this.props} user={user} />;
      }
    }

    WithUser = graphql(
      gql`
        query withUser {
          user {
            id
            email
            name
          }
        }
      `,
      {
        options: {
          fetchPolicy: "cache-first"
        }
      }
    )(WithUser);

    hoistNonReactStatic(WithUser, WrappedComponent);

    return WithUser;
  };
}
