const types = require("../types");
const TypeDeTerritoire = require("../../mongoose/TypeDeTerritoire");
const {
  GraphQLObjectType,
  GraphQLString,
  GraphQLID,
  GraphQLBoolean,
  GraphQLList,
  GraphQLInt
} = require("graphql");

module.exports = {
  createTypeDeTerritoire: {
    type: types.TypeDeTerritoire,
    args: {
      ...types.TypeDeTerritoire._typeConfig.fields()
    },
    resolve: async (_, { name, description }, context) => {
      const TypeDeTerritoire = new TypeDeTerritoire({ name, description });
      const result = await TypeDeTerritoire.save();
      return result;
    }
  }
};
