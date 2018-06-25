module.exports = {};
const {
  GraphQLObjectType,
  GraphQLString,
  GraphQLList,
  GraphQLID,
  GraphQLBoolean
} = require("graphql");

const EnumValue = new GraphQLObjectType({
  name: "EnumValue",
  fields: {
    id: { type: GraphQLID },
    label: { type: GraphQLString },
    description: { type: GraphQLString },
    deprecated: { type: GraphQLBoolean }
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
