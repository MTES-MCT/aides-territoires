import React from "react";
import AdminLayout from "../layouts/AdminLayout";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import GraphQLError from "../ui/GraphQLError";
import AppLoader from "../ui/AppLoader";
import injectSheet from "react-jss";
import classnames from "classnames";

class AdminPermissionsOverview extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    const { loading, allRoles, allPermissions, error } = this.props.data;
    if (error) return <GraphQLError error={error} />;
    if (loading) return <AppLoader />;
    return (
      <AdminLayout>
        <table className={classnames("table", this.props.classes.table)}>
          <thead>
            <tr>
              <th> </th>
              {allRoles.map(role => <th key={role.id}>{role.label}</th>)}
            </tr>
          </thead>
          <tbody>
            {allPermissions.map(permission => (
              <tr key={permission.id}>
                <td>{permission.label}</td>
                <td>
                  {allRoles[0].permissions.find(
                    rolePermission => rolePermission.id === permission.id
                  ) && "X"}
                </td>
                <td>
                  {allRoles[1].permissions.find(
                    rolePermission => rolePermission.id === permission.id
                  ) && "X"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </AdminLayout>
    );
  }
}

const styles = {
  table: {
    width: "100%"
  }
};

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
    allPermissions {
      id
      label
    }
  }
`;

export default compose(
  graphql(query),
  injectSheet(styles)
)(AdminPermissionsOverview);
