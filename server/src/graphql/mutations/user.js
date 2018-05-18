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
  saveUser: {
    type: types.user,
    args: {
      id: {type: GraphQLString},
      name: { type: GraphQLString },
      email: { type: GraphQLString },
      password: { type: GraphQLString }
    },
    resolve: (_, { from, text }, context) => {
      // pas d'id : on créer une nouvelle aide
      let result = null;
      if (!args.id) {
        const user = new UserModel(args);
        result = await user.save();
      }
      // un id, on le cherche puis on met à jour si on trouve
      let user = await UserModel.findById(args.id);
      if (user) {
        user = Object.assign(aide, args);
        result = user.save();
      }
      return result;
    }
  }
};
