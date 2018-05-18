import React from "react";
import AdminLayout from "modules/admin/layouts/AdminLayout";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import Loader from "modules/ui-kit/AppLoader";
import AideList from "modules/admin/presentationals/AideList";
import GraphQLError from "modules/ui-kit/GraphQLError";

const AideListPage = class extends React.Component {
  render() {
    const { loading, aides, error } = this.props.data;
    return (
      <AdminLayout>
        <h1 className="title is-1">Liste des aides</h1>
        {error && <GraphQLError error={error} />}
        {!aides && loading && <Loader />}
        {aides && (
          <AideList
            onDeleteClick={aide =>
              this.props.deleteAide({
                variables: { id: aide.id },
                refetchQueries: ["adminAllAides"]
              })
            }
            aides={aides}
          />
        )}
      </AdminLayout>
    );
  }
};

const allAidesQuery = gql`
  query adminAllAides {
    aides: allAides {
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
    }
  }
`;

const deleteAideMutation = gql`
  mutation deleteAide($id: ID) {
    deleteAide(id: $id) {
      n
      ok
    }
  }
`;

export default compose(
  graphql(allAidesQuery),
  graphql(deleteAideMutation, { name: "deleteAide" })
)(AideListPage);
