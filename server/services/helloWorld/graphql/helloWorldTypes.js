const graphql = require("graphql");
const helloService = require("../lib/helloService");

module.exports.queries = {
  helloWorld: {
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
        message: helloService.sayHello(name)
      };
    }
  }
};
