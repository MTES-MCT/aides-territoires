const graphql = require("graphql");

module.exports = {
  // describe our field for this type of entity
  type: new graphql.GraphQLObjectType({
    name: "helloWorld",
    fields: {
      message: { type: graphql.GraphQLString }
    }
  }),
  // `args` describes the arguments that our query accepts
  args: {
    name: { type: graphql.GraphQLString }
  },
  // data returned for this query
  resolve: function(_, { name }) {
    return {
      message: `hello ${name} !`
    };
  }
};
