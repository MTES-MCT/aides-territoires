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
console.log(JSON.stringify(types, null, 2));
module.exports = {
  AideSave: {
    type: types.Aide,
    args: {
      ...types.Aide._typeConfig.fields()
    },
    resolve: (_, { name, description }, context) => {
      const aide = new AideModel({ name, description });
      aide
        .save()
        .then(r => console.log(r))
        .catch(e => console.error(e));
      return {
        name: "name",
        description: "description"
      };
    }
  }
};
