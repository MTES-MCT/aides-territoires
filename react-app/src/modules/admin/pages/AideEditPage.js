import React from "react";
import AdminLayout from "modules/admin/layouts/AdminLayout";
import AideForm from "modules/admin/presentationals/AideForm";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";

const AideEditPage = ({ data }) => {
  return (
    <AdminLayout>
      <AideForm />
    </AdminLayout>
  );
};

const editAideQuery = gql`
  query editAide($id: ID) {
    getAide(id: $id) {
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
      console.log(props);
      return {
        variables: {
          id: props.match.params.id
        }
      };
    }
  })
)(AideEditPage);
