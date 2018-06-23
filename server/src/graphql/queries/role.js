const { GraphQLObjectType, GraphQLList } = require("graphql");
const types = require("../types");
const {
  userHasPermission,
  permissionDenied,
  getAllRoles
} = require("../../services/user");

module.exports = {
  allRoles: {
    type: new GraphQLObjectType({
      name: "allRoles",
      fields: {
        edges: {
          type: new GraphQLList(
            new GraphQLObjectType({
              name: "allRolesEdge",
              fields: {
                node: { type: types.Role }
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
      const allRoles = getAllRoles();
      result.edges = allRoles.map(role => {
        return {
          node: {
            ...role
          }
        };
      });
      return result;
    }
  }
};
