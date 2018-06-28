const { GraphQLString, GraphQLObjectType, GraphQLList } = require("graphql");
const { getAllEnums } = require("../../services/enums");
const types = require("../types");

module.exports = {
  allEnums: {
    type: new GraphQLObjectType({
      name: "allEnums",
      fields: {
        edges: {
          type: new GraphQLList(
            new GraphQLObjectType({
              name: "allEnumsEdges",
              fields: {
                userNodePermissions: { type: GraphQLList(GraphQLString) },
                node: { type: types.Enum }
              }
            })
          )
        }
      }
    }),
    resolve: (_, args, context) => {
      const results = {};
      results.edges = getAllEnums().map(enumeration => {
        // on générer pour chaque EnumValue type un identifiant unique "apolloCacheKey",
        // qui assurera qu'il n'y aura pas de conflit de mise en cache côté client.
        // Côté client, on créera un identificant de cache custom qui utilise apolloCacheKey.
        enumeration.values = enumeration.values.map(value => {
          return {
            ...value,
            apolloCacheKey: `${enumeration.id}_${value.id}`
          };
        });
        return {
          userNodePermissions: [],
          node: {
            ...enumeration
          }
        };
      });
      return results;
    }
  }
};
