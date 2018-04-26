module.exports = {};

const {
  GraphQLID,
  GraphQLObjectType,
  GraphQLNonNull,
  GraphQLString,
  GraphQLBoolean
} = require("graphql");

const TypeDeTerritoire = new GraphQLObjectType({
  name: "TypeDeTerritoire",
  fields: () => ({
    name: { type: GraphQLString },
    description: { type: GraphQLString }
  })
});

Object.assign(module.exports, { TypeDeTerritoire });
