module.exports = {};
const { GraphQLObjectType, GraphQLString } = require("graphql");

const Permission = new GraphQLObjectType({
  name: "permission",
  fields: {
    id: { type: GraphQLString },
    label: { type: GraphQLString }
  }
});

Object.assign(module.exports, { Permission });
