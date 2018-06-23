const { GraphQLObjectType, GraphQLList } = require("graphql");
const types = require("../types");
const {
  userHasPermission,
  permissionDenied,
  getAllRoles
} = require("../../services/user");

const AllRolesEdgesType = new GraphQLObjectType({
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
});

// a simple query to test our graphql AP
module.exports = {
  allRoles: {
    type: AllRolesEdgesType,
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
