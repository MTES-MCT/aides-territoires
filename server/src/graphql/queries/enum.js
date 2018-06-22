const { GraphQLString, GraphQLObjectType, GraphQLList } = require("graphql");
const enumsAide = require("../../enums/aide");

const enumType = new GraphQLObjectType({
  name: "allEnums",
  fields: {
    id: { type: GraphQLString },
    name: { type: GraphQLString },
    enums: {
      type: GraphQLList(
        new GraphQLObjectType({
          name: "enum",
          fields: {
            value: { type: GraphQLString },
            label: { type: GraphQLString }
          }
        })
      )
    }
  }
});

// a simple query to test our graphql API
module.exports = {
  allEnums: {
    type: GraphQLList(enumType),
    resolve: (_, args, context) => {
      const results = [];
      Object.keys(enumsAide).forEach(key => {
        results.push({
          id: key,
          name: key,
          enums: enumsAide[key]
        });
      });
      return results;
    }
  }
};
