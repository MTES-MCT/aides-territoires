import React from "react";
import AdminLayout from "../layouts/AdminLayout";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import GraphQLError from "../ui/GraphQLError";
import AppLoader from "../ui/AppLoader";
import injectSheet from "react-jss";
import classnames from "classnames";
import IconChecked from "material-ui/svg-icons/action/done";

class AdminPermissionsOverview extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  roleHasPermission(role, permissionId) {
    return role.permissions.find(
      rolePermission => rolePermission.id === permissionId
    );
  }
  render() {
    const { loading, allRoles, allPermissions, error } = this.props.data;
    return (
      <AdminLayout>
        <h1 className="title is-1">Permissions et rôles</h1>
        {error && <GraphQLError error={error} />}
        {loading && <AppLoader />}
        {!loading &&
          allPermissions && (
            <table className={classnames("table", this.props.classes.table)}>
              <thead>
                <tr>
                  <th> </th>
                  {allRoles.edges.map(role => (
                    <th key={role.node.id}>{role.node.label}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {allPermissions.edges.map(permission => (
                  <tr key={permission.node.id}>
                    <td>{permission.node.label}</td>
                    {allRoles.edges.map(role => (
                      <td key={role.node.id}>
                        {this.roleHasPermission(
                          role.node,
                          permission.node.id
                        ) && <IconChecked />}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          )}
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
      edges {
        node {
          label
          id
          permissions {
            label
            id
          }
        }
      }
    }
    allPermissions {
      edges {
        node {
          label
          id
        }
      }
    }
  }
`;

export default compose(
  graphql(query),
  injectSheet(styles)
)(AdminPermissionsOverview);
