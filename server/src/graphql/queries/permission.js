const { GraphQLString, GraphQLObjectType, GraphQLList } = require("graphql");
const permissionsAndRoles = require("../../config/permissions");
const { userHasPermission, permissionDenied } = require("../../services/user");
// a simple query to test our graphql API
module.exports = {
  allRoles: {
    type: new GraphQLList(
      new GraphQLObjectType({
        name: "role",
        fields: {
          id: { type: GraphQLString },
          label: { type: GraphQLString },
          permissions: {
            type: new GraphQLList(
              new GraphQLObjectType({
                name: "permission",
                fields: {
                  id: { type: GraphQLString },
                  label: { type: GraphQLString }
                }
              })
            )
          }
        }
      })
    ),
    resolve: (_, args, context) => {
      if (!userHasPermission(context.user, "see_permission_overview")) {
        permissionDenied();
      }
      let { roles, permissions } = permissionsAndRoles;
      roles.forEach(role => {
        role.permissions.forEach((permissionId, index) => {
          role.permissions[index] = permissions.find(
            permission => permission.id === permissionId
          );
        });
      });
      return roles;
    }
  }
};
