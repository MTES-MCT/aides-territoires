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
    resolve: (_, args, context) => {
      return {
        id: "56789YHJKNKL",
        name: "Yann"
      };
    }
  },
  users: {
    type: new GraphQLList(types.User),
    args: {
      limit: {
        type: GraphQLInt
      }
    },
    resolve: (_, args, context) => {
      return [
        {
          id: "56789YHJKNKL",
          name: "Yann"
        },
        {
          id: "56789YHJKNKl",
          name: "Samuel"
        }
      ];
    }
  }
};
