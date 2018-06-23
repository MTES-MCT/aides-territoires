module.exports = {};
const {
  GraphQLObjectType,
  GraphQLString,
  GraphQLList,
  GraphQLID
} = require("graphql");

const EnumValue = new GraphQLObjectType({
  name: "EnumType",
  fields: {
    id: { type: GraphQLString },
    label: { type: GraphQLString },
    description: { type: GraphQLString }
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
