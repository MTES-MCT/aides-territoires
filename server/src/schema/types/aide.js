module.exports = {};

const {
  GraphQLID,
  GraphQLObjectType,
  GraphQLNonNull,
  GraphQLString,
  GraphQLBoolean
} = require("graphql");

const Aide = new GraphQLObjectType({
  name: "Aide",
  fields: () => ({
    name: { type: GraphQLString },
    description: { type: GraphQLString }
  })
});

Object.assign(module.exports, { Aide });
