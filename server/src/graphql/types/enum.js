module.exports = {};
const {
  GraphQLObjectType,
  GraphQLString,
  GraphQLList,
  GraphQLID,
  GraphQLNonNull
} = require("graphql");

const EnumValue = new GraphQLObjectType({
  name: "EnumValue",
  fields: {
    id: { type: GraphQLNonNull(GraphQLID) },
    label: { type: GraphQLNonNull(GraphQLString) },
    description: { type: GraphQLString },
    apolloCacheKey: { type: GraphQLNonNull(GraphQLString) }
  }
});

const Enum = new GraphQLObjectType({
  name: "Enum",
  fields: {
    id: { type: GraphQLID },
    label: { type: GraphQLString },
    values: { type: new GraphQLList(EnumValue) }
  }
});

Object.assign(module.exports, { Enum, EnumValue });
