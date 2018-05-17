import React from "react";
import AdminLayout from "modules/admin/layouts/AdminLayout";
import AideForm from "modules/admin/forms/AideForm";
import AppLoader from "modules/ui-kit/AppLoader";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import GraphQLError from "modules/ui-kit/GraphQLError";

const AideEditPage = ({ data: { aide, error, loading } }) => {
  return (
    <AdminLayout>
      {error && <GraphQLError error={error} />}
      {loading && <AppLoader />}
      {aide && <AideForm operation={"edition"} aide={aide} />}
    </AdminLayout>
  );
};

const editAideQuery = gql`
  query editAide($id: ID) {
    aide: getAide(id: $id) {
      id
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
      tauxSubvention
      contact
      status
      categorieParticuliere
    }
  }
`;

export default compose(
  graphql(editAideQuery, {
    options: props => {
      return {
        variables: {
          id: props.match.params.id
        }
      };
    }
  })
)(AideEditPage);
