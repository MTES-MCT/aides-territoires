const { sendContactFormEmail } = require("../../services/email");
const types = require("../types");
const {
  GraphQLObjectType,
  GraphQLString,
  GraphQLID,
  GraphQLBoolean,
  GraphQLList,
  GraphQLInt
} = require("graphql");

module.exports = {
  sendContactFormEmail: {
    type: types.sendContactFormEmail,
    args: {
      from: { type: GraphQLString },
      text: { type: GraphQLString }
    },
    resolve: (_, { from, text }, context) => {
      sendContactFormEmail({ from, text });
      return {
        from,
        text
      };
    }
  }
};
