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
const { getEnumAsGraphQLEnumType } = require("../../enumTypes");
const aideEtapes = getEnumAsGraphQLEnumType(
  "SEARCH_AIDE_ETAPES",
  "AIDE_ETAPES"
);

module.exports = {
  getAide: {
    type: types.Aide,
    args: {
      id: {
        type: GraphQLID
      }
    },
    resolve: async (_, { id }, context) => {
      return await AideModel.findById(id);
    }
  },
  allAides: {
    type: new GraphQLList(types.Aide),
    args: {
      ...types.Aide._typeConfig.fields()
    },
    resolve: async (_, args = {}, context) => {
      // console.log(JSON.stringify(args, null, 2));
      const result = await AideModel.find({});
      console.log(result);
      return result;
      /*
      const query = AideModel.find(args);
      if (args.limit) {
        query.limit(args.limit);
      }
      query.sort("-createdAt");
      return query;
      */
    }
  },
  searchAides: {
    type: new GraphQLList(types.Aide),
    args: {
      etape: {
        type: new GraphQLList(aideEtapes)
      }
    },
    resolve: async (_, args = {}, context) => {
      const result = await AideModel.find(args);
      return result;
    }
  }
};
