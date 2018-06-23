import React from "react";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import hoistNonReactStatic from "hoist-non-react-statics";
import AppLoader from "../ui/AppLoader";
import GraphQLError from "../ui/GraphQLError";

const getDisplayName = WrappedComponent =>
  WrappedComponent.displayName || WrappedComponent.name || "Component";

export default function withEnums(options = {}) {
  return WrappedComponent => {
    class WithEnums extends React.Component {
      static displayName = `WithEnums(${getDisplayName(WrappedComponent)})`;

      // formater les enums pour que le composant décorés
      // puisse simple ecrires enums.perimetre.label, pour avoir
      // le label de l'enum perimetre, et enums.perimetre.values pour avoir les valeurs
      formatEnums = () => {
        // create a brand new object to avoid mutations on enums
        // stored in apollo cache
        const enumerations = {};
        if (this.props.data.loading) return enumerations;
        this.props.data.enums.edges.forEach(edge => {
          enumerations[edge.node.id] = {
            id: edge.node.id,
            label: edge.node.label,
            values: edge.node.values
          };
        });
        return enumerations;
      };

      render() {
        const {
          data: { loading, error, allEnums }
        } = this.props;
        if (loading) return null;
        if (error) return <GraphQLError error={error} />;
        return <WrappedComponent {...this.props} enums={this.formatEnums()} />;
      }
    }

    WithEnums = graphql(
      gql`
        query allEnums {
          enums: allEnums {
            edges {
              node {
                id
                label
                values {
                  id
                  label
                }
              }
            }
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
    )(WithEnums);

    hoistNonReactStatic(WithEnums, WrappedComponent);

    return WithEnums;
  };
}
