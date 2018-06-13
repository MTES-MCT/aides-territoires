const types = require("../types");
const {
  GraphQLObjectType,
  GraphQLString,
  GraphQLID,
  GraphQLBoolean,
  GraphQLList,
  GraphQLInt
} = require("graphql");

module.exports = {
  user: {
    type: types.User,
    args: {
      id: {
        type: GraphQLID
      }
    },
    resolve: (_, args, { user }) => user
  }
};
