module.exports = {};

const {
  GraphQLID,
  GraphQLObjectType,
  GraphQLNonNull,
  GraphQLEnumType,
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
    perimetreApplication: { type: new GraphQLList(GraphQLString) },
    etape: { type: new GraphQLList(GraphQLString) },
    status: { type: GraphQLString },
    perimetreApplication: { type: new GraphQLList(GraphQLString) },
    structurePorteuse: { type: GraphQLString }
  })
});

Object.assign(module.exports, { Aide });
