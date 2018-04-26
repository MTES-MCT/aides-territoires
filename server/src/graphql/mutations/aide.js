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
    resolve: async (_, { name, description }, context) => {
      const aide = new AideModel({ name, description });
      const result = await aide.save();
      return result;
    }
  }
};
