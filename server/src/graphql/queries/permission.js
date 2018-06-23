const { GraphQLString, GraphQLObjectType, GraphQLList } = require("graphql");
const {
  userHasPermission,
  permissionDenied,
  getAllRoles,
  getAllPermissions
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

const AllRolesEdgesType = new GraphQLObjectType({
  name: "allRoles",
  fields: {
    edges: {
      type: new GraphQLList(
        new GraphQLObjectType({
          name: "allRolesEdge",
          fields: {
            node: { type: RoleType }
          }
        })
      )
    }
  }
});

const AllPermissionsEdgesType = new GraphQLObjectType({
  name: "allPermissions",
  fields: {
    edges: {
      type: new GraphQLList(
        new GraphQLObjectType({
          name: "allPermissionsEdge",
          fields: {
            node: { type: PermissionType }
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
        // permissionDenied();
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
  },
  allPermissions: {
    type: AllPermissionsEdgesType,
    resolve: (_, args, context) => {
      if (!userHasPermission(context.user, "see_permissions_overview")) {
        // permissionDenied();
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
