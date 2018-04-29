module.exports = {};

const {
  GraphQLID,
  GraphQLObjectType,
  GraphQLNonNull,
  GraphQLEnumType,
  GraphQLInt,
  GraphQLString,
  GraphQLBoolean,
  GraphQLList
} = require("graphql");

const Aide = new GraphQLObjectType({
  name: "Aide",
  fields: () => ({
    id: { type: GraphQLString },
    name: { type: GraphQLString },
    createdAt: { type: GraphQLString },
    updatedAt: { type: GraphQLString },
    description: { type: GraphQLString },
    type: { type: GraphQLString },
    perimetreApplicationType: { type: GraphQLString },
    perimetreApplicationName: { type: GraphQLString },
    perimetreApplicationCode: { type: GraphQLString },
    perimetreDiffusionType: { type: GraphQLString },
    lien: { type: GraphQLString },
    etape: { type: GraphQLString },
    status: { type: GraphQLString },
    structurePorteuse: { type: GraphQLString },
    beneficiaires: { type: GraphQLList(GraphQLString) },
    populationMin: { type: GraphQLInt },
    populationMax: { type: GraphQLInt },
    status: { type: GraphQLString }
  })
});

Object.assign(module.exports, { Aide });
