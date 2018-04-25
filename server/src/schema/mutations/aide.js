const types = require("../types");
const {
  GraphQLObjectType,
  GraphQLString,
  GraphQLID,
  GraphQLBoolean,
  GraphQLList,
  GraphQLInt
} = require("graphql");
console.log(JSON.stringify(types, null, 2));
module.exports = {
  AideSave: {
    type: types.Aide,
    args: {
      ...types.Aide._typeConfig.fields()
    },
    resolve: (_, { name, description }, context) => {
      return {
        name: "name",
        description: "description"
      };
    }
  }
};
