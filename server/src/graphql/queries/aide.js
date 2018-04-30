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
const { enums, formatEnumForGraphQL } = require("../../enums");
const aideEtapes = formatEnumForGraphQL("searchAideEtapes", enums.AIDE_ETAPES);
const aideStatusPublication = formatEnumForGraphQL(
  "searchAideStatusPublicaton",
  enums.AIDE_STATUS_PUBLICATION
);
const aideApplicationTypes = formatEnumForGraphQL(
  "searchApplicationTypes",
  enums.AIDE_PERIMETRE_APPLICATION_TYPES
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
      const result = await AideModel.find({});
      return result;
    }
  },
  searchAides: {
    type: new GraphQLList(types.Aide),
    args: {
      etape: {
        type: new GraphQLList(aideEtapes)
      },
      status: {
        type: new GraphQLList(aideStatusPublication)
      },
      perimetreApplicationType: {
        type: new GraphQLList(aideApplicationTypes)
      }
    },
    resolve: async (_, args = {}, context) => {
      const result = await AideModel.find(args);
      return result;
    }
  }
};
