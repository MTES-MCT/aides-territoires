const { GraphQLObjectType, GraphQLList } = require("graphql");
const types = require("../types");
const {
  userHasPermission,
  permissionDenied,
  getAllPermissions
} = require("../../services/user");

// a simple query to test our graphql AP
module.exports = {
  allPermissions: {
    type: new GraphQLObjectType({
      name: "allPermissions",
      fields: {
        edges: {
          type: new GraphQLList(
            new GraphQLObjectType({
              name: "allPermissionsEdge",
              fields: {
                node: { type: types.Permission }
              }
            })
          )
        }
      }
    }),
    resolve: (_, args, context) => {
      if (!userHasPermission(context.user, "see_permissions_overview")) {
        permissionDenied();
      }
      const result = {};
      result.edges = getAllPermissions().map(permission => {
        return {
          node: {
            ...permission
          }
        };
      });
      return result;
    }
  }
};
