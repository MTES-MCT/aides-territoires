import React, { Component } from "react";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import AppLoader from "modules/ui-kit/AppLoader";
import PropTypes from "prop-types";
import GraphQLError from "modules/ui-kit/GraphQLError";

const searchAidesQuery = gql`
  query searchAidesQuery(
    $etape: [searchAideEtapes]
    $type: [searchAideTypes]
    $statusPublication: [searchAideStatusPublication]
    $perimetreApplicationType: [searchAidePerimetreApplicationType]
  ) {
    aides: searchAides(
      etape: $etape
      type: $type
      statusPublication: $statusPublication
      perimetreApplicationType: $perimetreApplicationType
    ) {
      id
      noms
      createdAt
      updatedAt
      descriptionA
      perimetreApplicationType
      perimetreApplicationNom
      perimetreApplicationCode
      perimetreDiffusionType
      etape
      structurePorteuse
      statusPublication
      lien
      type
      beneficiaires
    }
  }
`;

export default WrappedComponent => {
  class AidesProvider extends Component {
    static propTypes = {
      perimetreApplicationType: PropTypes.string,
      perimetreApplicationCode: PropTypes.string,
      statusPublication: PropTypes.array,
      type: PropTypes.array
    };
    render() {
      if (this.props.data.loading) {
        return <div>Chargement ...</div>;
      }
      if (this.props.data.error) {
        return <GraphQLError error={this.props.data.error} />;
      }
      return (
        <div>
          <WrappedComponent {...this.props} aides={this.props.data.aides} />
        </div>
      );
    }
  }
  return compose(
    graphql(searchAidesQuery, {
      options: props => {
        const variables = {};
        if (props.etape && props.etape.length > 0) {
          variables.etape = props.etape;
        }
        if (props.type && props.type.length > 0) {
          variables.type = props.type;
        }
        if (props.statusPublication) {
          variables.statusPublication = props.statusPublication;
        }
        if (
          props.perimetreApplicationType &&
          props.perimetreApplicationType.length > 0
        ) {
          variables.perimetreApplicationType = props.perimetreApplicationType;
        }
        return {
          variables
        };
      }
    })
  )(AidesProvider);
};
