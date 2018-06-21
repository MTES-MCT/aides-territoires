const { GraphQLString, GraphQLObjectType, GraphQLList } = require("graphql");
const {
  userHasPermission,
  permissionDenied,
  getAllRoles
} = require("../../services/user");

const PermissionType = new GraphQLObjectType({
  name: "permission",
  fields: {
    id: { type: GraphQLString },
    label: { type: GraphQLString }
  }
});

const RoleType = new GraphQLObjectType({
  name: "role",
  fields: {
    id: { type: GraphQLString },
    label: { type: GraphQLString },
    permissions: {
      type: new GraphQLList(PermissionType)
    }
  }
});

// a simple query to test our graphql API
module.exports = {
  allRoles: {
    type: new GraphQLList(RoleType),
    resolve: (_, args, context) => {
      if (!userHasPermission(context.user, "see_permission_overview")) {
        permissionDenied();
      }
      return getAllRoles();
    }
  }
};
