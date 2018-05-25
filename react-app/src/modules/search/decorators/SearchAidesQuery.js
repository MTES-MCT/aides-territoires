import React, { Component } from "react";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import AppLoader from "modules/ui-kit/AppLoader";
import PropTypes from "prop-types";
import GraphQLError from "modules/ui-kit/GraphQLError";
import { searchFiltersAreEmpty } from "../../../services/searchLib";

const query = gql`
  query searchAidesQuery($filters: allAidesFilters) {
    aides: allAides(sort: createdAtDesc, filters: $filters) {
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
      destination
      thematiques
      dateEcheance
    }
  }
`;

class SearchAideQuery extends Component {
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
  graphql(query, {
    options: ({ filters }) => {
      filters = searchFiltersAreEmpty(filters) ? {} : filters;
      return {
        variables: {
          filters
        }
      };
    }
  })
)(SearchAideQuery);
