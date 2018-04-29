import React from "react";
import AdminLayout from "modules/admin/layouts/AdminLayout";
import AideForm from "modules/admin/forms/AideForm";
import AppLoader from "modules/common/presentationals/AppLoader";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";

const AideEditPage = ({ data: { aide } }) => {
  return (
    <AdminLayout>
      {!aide && <AppLoader />}
      {aide && <AideForm operation={"edition"} aide={aide} />}
    </AdminLayout>
  );
};

const editAideQuery = gql`
  query editAide($id: ID) {
    aide: getAide(id: $id) {
      id
      name
      description
      etape
      type
      updatedAt
      createdAt
      beneficiaires
      structurePorteuse
      perimetreApplication
      perimetreApplicationCode
      populationMin
      populationMax
      perimetreDiffusion
      status
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
