const { GraphQLString, GraphQLObjectType, GraphQLList } = require("graphql");
const permissionsAndRoles = require("../../config/permissions");
// a simple query to test our graphql API
module.exports = {
  allRoles: {
    type: new GraphQLList(
      new GraphQLObjectType({
        name: "role",
        fields: {
          id: { type: GraphQLString },
          label: { type: GraphQLString },
          permissions: { type: new GraphQLList(GraphQLString) }
        }
      })
    ),
    resolve: (_, args, context = {}) => {
      return [
        {
          id: "oucou",
          label: "hello",
          permissions: ["oueoue", "uoefrt", "ufoeutoue"]
        }
      ];
    }
  }
};
