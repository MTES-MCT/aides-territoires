module.exports = {};

const { GraphQLString, GraphQLObjectType } = require("graphql");

const Hello = new GraphQLObjectType({
  name: "Hello",
  fields: () => ({
    message: {
      type: GraphQLString
    }
  })
});

Object.assign(module.exports, { Hello });
