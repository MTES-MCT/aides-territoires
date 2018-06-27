import React, { Component } from "react";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import AppLoader from "../ui/AppLoader";
import PropTypes from "prop-types";
import GraphQLError from "../ui/GraphQLError";

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
    if (this.props.data.allAides) {
      return <div>{this.props.children(this.props.data.allAides)}</div>;
    } else {
      return <div>Aucune aide trouvée</div>;
    }
  }
}

const query = gql`
  query adminAllAides($filters: allAidesFilters) {
    allAides(filters: $filters) {
      edges {
        meta {
          userUiPermissions
        }
        node {
          id
          auteur {
            id
            name
            roles
          }
          nom
          description
          criteresEligibilite
          etape
          type
          updatedAt
          createdAt
          structurePorteuse
          perimetreApplicationType
          perimetreApplicationNom
          perimetreApplicationCode
          populationMin
          populationMax
          perimetreDiffusionType
          perimetreDiffusionTypeAutre
          statusPublication
          lien
          beneficiaires
          beneficiairesAutre
          destination
          destinationAutre
          formeDeDiffusion
          formeDeDiffusionAutre
          thematiques
          dateDebut
          dateEcheance
          datePredepot
          tauxSubvention
          contact
          status
          categorieParticuliere
          demandeTiersPossible
          motsCles
        }
      }
    }
  }
`;

const queryOptions = {
  options: ({ filters }) => {
    return {
      variables: {
        filters
      }
    };
  }
};

export default compose(graphql(query, queryOptions))(AdminAllAidesQuery);
