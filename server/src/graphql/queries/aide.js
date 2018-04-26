const types = require("../types");
const AideModel = require("../../mongoose/Aide");
const {
  GraphQLObjectType,
  GraphQLString,
  GraphQLID,
  GraphQLBoolean,
  GraphQLList,
  GraphQLInt
} = require("graphql");

module.exports = {
  aide: {
    type: types.Aide,
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
  allAides: {
    type: new GraphQLList(types.Aide),
    args: {
      limit: {
        type: GraphQLInt
      }
    },
    resolve: (_, args, context) => {
      const query = AideModel.find({});
      if (args.limit) {
        query.limit(args.limit);
      }
      query.sort("-createdAt");
      return query.then(r => r);
    }
  }
};
