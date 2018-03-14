const graphql = require("graphql");
const sendEmail = require("../lib/email").sendEmail;

module.exports.mutations = {
  email: {
    // describe our field for this type of entity
    type: new graphql.GraphQLObjectType({
      name: "email",
      fields: {
        from: { type: graphql.GraphQLString },
        to: { type: graphql.GraphQLString },
        subject: { type: graphql.GraphQLString },
        text: { type: graphql.GraphQLString }
      }
    }),
    // `args` describes the arguments that our query accepts
    args: {
      from: { type: graphql.GraphQLString },
      to: { type: graphql.GraphQLString },
      subject: { type: graphql.GraphQLString },
      text: { type: graphql.GraphQLString }
    },
    // data returned for this query
    resolve: function(_, { from, to, subject, text }) {
      sendEmail({ from, to, subject, text });
      return {
        from,
        to,
        subject,
        text
      };
    }
  }
};
