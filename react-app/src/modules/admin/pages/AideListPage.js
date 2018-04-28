import React from "react";
import AdminLayout from "modules/admin/layouts/AdminLayout";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import Loader from "modules/common/presentationals/AppLoader";
import AideList from "modules/admin/presentationals/AideList";

const AideListPage = class extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { props } = this;

    const { loading, allAides } = props.data;
    return (
      <AdminLayout>
        <h1 className="title is-1">Liste des aides</h1>
        {loading && <Loader />}
        {loading === false && (
          <AideList
            onDeleteClick={aide =>
              this.props.deleteAide({
                variables: { id: aide.id },
                refetchQueries: ["adminAllAides"]
              })
            }
            aides={allAides}
          />
        )}
      </AdminLayout>
    );
  }
};

const allAidesQuery = gql`
  query adminAllAides {
    allAides {
      id
      createdAt
      updatedAt
      name
      description
      perimetreApplication
      perimetreApplicationCode
      etape
      structurePorteuse
      status
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
