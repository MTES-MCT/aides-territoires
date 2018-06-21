import React from "react";
import AdminLayout from "../layouts/AdminLayout";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import GraphQLError from "../ui/GraphQLError";
import AppLoader from "../ui/AppLoader";

class AdminPermissionsOverview extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    console.log(this.props);
    const { loading, allRoles, error } = this.props.data;
    if (error) return <GraphQLError error={error} />;
    if (loading) return <AppLoader />;
    return (
      <AdminLayout>
        <div>
          <p>Coucou</p>
        </div>
      </AdminLayout>
    );
  }
}

const query = gql`
  {
    allRoles {
      label
      id
      permissions {
        id
        label
      }
    }
  }
`;

export default compose(graphql(query))(AdminPermissionsOverview);
