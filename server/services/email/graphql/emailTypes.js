const graphql = require("graphql");
const { sendContactFormEmail } = require("../lib/email");

module.exports.mutations = {
  sendContactFormEmail: {
    // describe our field for this type of entity
    type: new graphql.GraphQLObjectType({
      name: "email",
      fields: {
        from: { type: graphql.GraphQLString },
        text: { type: graphql.GraphQLString }
      }
    }),
    // `args` describes the arguments that our query accepts
    args: {
      from: { type: graphql.GraphQLString },
      text: { type: graphql.GraphQLString }
    },
    // data returned for this query
    resolve: function(_, { from, text }) {
      sendContactFormEmail({ from, text });
      return {
        from,
        text
      };
    }
  }
};
