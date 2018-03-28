const userTypes = require("../types/user");
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
    type: userTypes.User,
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
    type: new GraphQLList(userTypes.User),
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
