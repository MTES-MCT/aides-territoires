const { GraphQLString, GraphQLObjectType, GraphQLList } = require("graphql");
const { getAllEnums } = require("../../services/enums");

function getAllEnumsType() {
  return new GraphQLObjectType({
    name: "allEnums",
    fields: {
      hello: { type: GraphQLString },
      edges: { type: new GraphQLList(getAllEnumsEdgesType()) }
    }
  });
}

function getAllEnumsEdgesType() {
  return new GraphQLObjectType({
    name: "allEnumsEdges",
    fields: {
      userNodePermissions: { type: GraphQLList(GraphQLString) },
      node: { type: getEnumNodeType() }
    }
  });
}

function getEnumNodeType() {
  return new GraphQLObjectType({
    name: "enumNodeType",
    fields: {
      id: { type: GraphQLString },
      label: { type: GraphQLString },
      values: { type: GraphQLList(getEnumValueType()) }
    }
  });
}

function getEnumValueType() {
  return new GraphQLObjectType({
    name: "enumValueType",
    fields: {
      id: { type: GraphQLString },
      label: { type: GraphQLString },
      description: { type: GraphQLString }
    }
  });
}

module.exports = {
  allEnums: {
    type: getAllEnumsType(),
    resolve: (_, args, context) => {
      const allEnums = getAllEnums();
      const results = {};
      results.edges = allEnums.map(enumeration => {
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
