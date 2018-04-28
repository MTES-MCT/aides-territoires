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
  saveAide: {
    type: types.Aide,
    args: {
      ...types.Aide._typeConfig.fields()
    },
    resolve: async (_, args, context) => {
      // pas d'id : on créer une nouvelle aide
      let result = null;
      if (!args.id) {
        const aide = new AideModel(args);
        result = await aide.save();
      }
      // un id, on le cherche puis on met à jour si on trouve
      let aide = await AideModel.findById(args.id);
      if (aide) {
        aide = Object.assign(aide, args);
        result = aide.save();
      }
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
