module.exports = {};

const {
  GraphQLID,
  GraphQLObjectType,
  GraphQLNonNull,
  GraphQLString,
  GraphQLBoolean
} = require("graphql");

const sendContactFormEmail = new GraphQLObjectType({
  name: "sendContactFormEmail",
  fields: () => ({
    from: { type: GraphQLString },
    text: { type: GraphQLString }
  })
});

Object.assign(module.exports, { sendContactFormEmail });
