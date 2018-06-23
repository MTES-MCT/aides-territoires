const { GraphQLString, GraphQLObjectType, GraphQLList } = require("graphql");
const enums = require("../../config/enums");

const enumOptionType = new GraphQLObjectType({
  name: "enum",
  fields: {
    value: { type: GraphQLString },
    label: { type: GraphQLString }
  }
});

const enumType = new GraphQLObjectType({
  name: "allEnums",
  fields: {
    id: { type: GraphQLString },
    label: { type: GraphQLString },
    options: {
      type: GraphQLList(enumOptionType)
    }
  }
});

module.exports = {
  allEnums: {
    type: GraphQLList(enumType),
    resolve: (_, args, context) => {
      return enums;
    }
  }
};
