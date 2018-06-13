const types = require("../types");
const User = require("../../mongoose/User");
const { getUserByPassword, getJwt } = require("../../services/user");

const {
  GraphQLNonNull,
  GraphQLObjectType,
  GraphQLString,
  GraphQLID,
  GraphQLBoolean,
  GraphQLList,
  GraphQLInt
} = require("graphql");

module.exports = {
  login: {
    type: new GraphQLObjectType({
      name: "LoginResult",
      fields: () => ({
        jwt: {
          type: new GraphQLNonNull(GraphQLString),
          description: "The Json Web Token"
        },
        user: {
          type: types.User
        }
      })
    }),
    args: {
      email: { type: new GraphQLNonNull(GraphQLString) },
      password: { type: new GraphQLNonNull(GraphQLString) }
    },
    resolve: async (_, { email, password }, context) => {
      const user = await getUserByPassword(email, password);

      if (!user) throw new Error("Wrong login / password");

      return {
        jwt: await getJwt(user),
        user
      };
    }
  }
};
