module.exports = {};

const {
  GraphQLObjectType,

  GraphQLString
} = require("graphql");

const sendContactFormEmail = new GraphQLObjectType({
  name: "sendContactFormEmail",
  fields: () => ({
    from: { type: GraphQLString },
    text: { type: GraphQLString }
  })
});

Object.assign(module.exports, { sendContactFormEmail });
