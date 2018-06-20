module.exports = {};
const { getRoleById } = require("../../services/user");
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
      type: new GraphQLList(GraphQLString),
      resolve: user => {
        return user.roles.map(role => getRoleById(role).label);
      }
    }
  })
});

Object.assign(module.exports, { User });
