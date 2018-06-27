import React from "react";
import AdminLayout from "../layouts/AdminLayout";
import AideForm from "./AdminAideForm";
import AppLoader from "../ui/AppLoader";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import GraphQLError from "../ui/GraphQLError";

const AideEditPage = ({ data: { aide, error, loading } }) => {
  return (
    <AdminLayout>
      {error && <GraphQLError error={error} />}
      {loading && <AppLoader />}
      {!loading && aide && <AideForm operation={"edition"} aide={aide.node} />}
    </AdminLayout>
  );
};

const query = gql`
  query editAide($id: ID) {
    aide: getAide(id: $id) {
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
`;

export default compose(
  graphql(query, {
    options: props => {
      return {
        variables: {
          id: props.match.params.id
        }
      };
    }
  })
)(AideEditPage);
