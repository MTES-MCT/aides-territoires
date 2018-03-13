const graphql = require("graphql");

module.exports = {
  // describe our field for this type of entity
  type: new graphql.GraphQLObjectType({
    name: "aide",
    fields: {
      id: { type: graphql.GraphQLString },
      title: { type: graphql.GraphQLString },
      description: { type: graphql.GraphQLString }
    }
  }),
  // `args` describes the arguments that our query accepts
  args: {
    id: { type: graphql.GraphQLString }
  },
  // data returned for this query
  resolve: function(_, { id }) {
    return {
      id: id,
      title: "aide de test",
      description: "description aide de test"
    };
  }
};
