module.exports = {};
const {
  GraphQLID,
  GraphQLObjectType,
  GraphQLNonNull,
  GraphQLString,
  GraphQLList
} = require("graphql");

const User = new GraphQLObjectType({
  name: "User",
  fields: () => ({
    id: { type: new GraphQLNonNull(GraphQLID) },
    name: { type: new GraphQLNonNull(GraphQLString) },
    email: {
      type: GraphQLString
    },
    roles: {
      type: new GraphQLList(GraphQLString)
    },
    permissions: { type: new GraphQLList(GraphQLString) }
  })
});

Object.assign(module.exports, { User });
