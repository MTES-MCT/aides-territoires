import React, { Component } from "react";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import AppLoader from "modules/ui-kit/AppLoader";
import PropTypes from "prop-types";
import GraphQLError from "modules/ui-kit/GraphQLError";

const searchAidesQuery = gql`
  query allAidesQuery(
    $etape: [allAidesEtape]
    $type: [allAidesType]
    $statusPublication: [allAidesStatusPublication]
    $perimetreApplicationType: [allAidesPerimetreApplicationType]
    $perimetreApplicationCode: String
    $formeDeDiffusion: [allAidesFormeDeDiffusion]
    $thematiques: [allAidesThematiques]
  ) {
    aides: allAides(
      sort: createdAtDesc
      filters: {
        etape: $etape
        type: $type
        statusPublication: $statusPublication
        perimetreApplicationType: $perimetreApplicationType
        perimetreApplicationCode: $perimetreApplicationCode
        formeDeDiffusion: $formeDeDiffusion
        thematiques: $thematiques
      }
    ) {
      id
      nom
      createdAt
      updatedAt
      description
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
      formeDeDiffusion
    }
  }
`;

class AidesSearchQuery extends Component {
  static propTypes = {
    children: PropTypes.func.isRequired,
    perimetreApplicationType: PropTypes.string,
    perimetreApplicationCode: PropTypes.string,
    etape: PropTypes.array,
    statusPublication: PropTypes.array,
    type: PropTypes.array
  };
  render() {
    if (this.props.data.loading) {
      return <AppLoader />;
    }
    if (this.props.data.error) {
      return <GraphQLError error={this.props.data.error} />;
    }
    return <div>{this.props.children(this.props.data)}</div>;
  }
}
export default compose(
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
      if (props.perimetreApplicationCode) {
        variables.perimetreApplicationCode = props.perimetreApplicationCode;
      }
      if (props.formeDeDiffusion && props.formeDeDiffusion.length > 0) {
        variables.formeDeDiffusion = props.formeDeDiffusion;
      }
      if (props.thematiques && props.thematiques.length > 0) {
        variables.thematiques = props.thematiques;
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
)(AidesSearchQuery);
