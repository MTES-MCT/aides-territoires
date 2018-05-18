module.exports = {};
const { GraphQLString } = require("graphql");

const Enum = new GraphQLObjectType({
  name: "Enum",
  fields: () => ({
    value: { type: GraphQLString },
    label: { type: GraphQLString }
  })
});

Object.assign(module.exports, { Enum });
