const { GraphQLString, GraphQLObjectType, GraphQLList } = require("graphql");
const permissionsAndRoles = require("../../config/permissions");
const {
  userHasPermission,
  permissionDenied,
  getPermissionById
} = require("../../services/user");
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
        //permissionDenied();
      }
      let { roles } = permissionsAndRoles;
      let results = [];
      roles.forEach(role => {
        let newRole = {
          ...role,
          permissions: role.permissions.map(getPermissionById)
        };
        results.push(newRole);
      });
      return results;
    }
  }
};
