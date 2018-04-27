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
  createAide: {
    type: types.Aide,
    args: {
      ...types.Aide._typeConfig.fields()
    },
    resolve: async (_, args, context) => {
      const aide = new AideModel(args);
      const result = await aide.save();
      return result;
    }
  },
  deleteAide: {
    type: new GraphQLObjectType({
      name: "deleteAide",
      fields: () => ({
        id: { type: GraphQLString },
        n: { type: GraphQLString },
        ok: { type: GraphQLString }
      })
    }),
    args: {
      id: {
        type: GraphQLID
      }
    },
    resolve: async (_, { id }, context) => {
      const result = await AideModel.remove({ _id: id });
      return { id, ...result };
    }
  }
};
