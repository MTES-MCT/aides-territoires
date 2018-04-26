module.exports = {};

const {
  GraphQLID,
  GraphQLObjectType,
  GraphQLNonNull,
  GraphQLString,
  GraphQLBoolean
} = require("graphql");

const User = new GraphQLObjectType({
  name: "User",
  fields: () => ({
    id: {
      type: new GraphQLNonNull(GraphQLID)
    },
    name: {
      type: GraphQLString,
      args: {
        uppercase: {
          type: GraphQLBoolean
        }
      },
      resolve: (user, { uppercase }, context) => {
        return uppercase ? user.name.toUpperCase() : user.name;
      }
    }
  })
});

Object.assign(module.exports, { User });
