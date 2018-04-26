import React from "react";
import AdminLayout from "modules/admin/layouts/AdminLayout";
import { graphql } from "react-apollo";
import gql from "graphql-tag";
import Loader from "modules/common/presentationals/AppLoader";
import AideList from "modules/admin/presentationals/AideList";

const AideListPage = props => {
  const { loading, allAides } = props.data;
  return (
    <AdminLayout>
      <h1 className="title is-1">Liste des aides</h1>
      {loading && <Loader />}
      {loading === false && <AideList aides={allAides} />}
    </AdminLayout>
  );
};

export const allAidesQuery = gql`
  query AideListPageAllAides {
    allAides {
      id
      createdAt
      updatedAt
      name
      description
    }
  }
`;

export default graphql(allAidesQuery)(AideListPage);
