import React, { Component } from "react";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import AppLoader from "../ui/AppLoader";
import PropTypes from "prop-types";
import GraphQLError from "../ui/GraphQLError";
import { cleanSearchFilters } from "../../lib/search";

class AdminAllAidesQuery extends Component {
  static propTypes = {
    children: PropTypes.func.isRequired
  };
  render() {
    if (this.props.data.loading) {
      return <AppLoader />;
    }
    if (this.props.data.error) {
      return <GraphQLError error={this.props.data.error} />;
    }
    return <div>{this.props.children(this.props.data.allAides)}</div>;
  }
}

const query = gql`
  query adminAllAides($filters: allAidesFilters) {
    allAides(filters: $filters) {
      edges {
        meta {
          userPermissions
        }
        node {
          id
          createdAt
          updatedAt
          nom
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
          destination
          destinationAutre
          formeDeDiffusion
          formeDeDiffusionAutre
          beneficiaires
          categorieParticuliere
          demandeTiersPossible
          auteur {
            id
            name
            roles
          }
        }
      }
    }
  }
`;

export default compose(
  graphql(query, {
    options: ({ filters }) => {
      let newFilters = { ...filters };
      newFilters = cleanSearchFilters(newFilters);

      if (newFilters.dateEcheance) {
        newFilters.dateEcheance = {
          operator: "gte",
          value: newFilters.dateEcheance
        };
      }
      // ces champs sont concaténés par le reducer custom pour créer
      // le champ dateEcheance,
      // on ne veut pas les envoyer en tant que filtres à notre requête
      delete newFilters.dateEcheanceMonth;
      delete newFilters.dateEcheanceYear;
      return {
        variables: {
          filters: newFilters
        }
      };
    }
  })
)(AdminAllAidesQuery);
