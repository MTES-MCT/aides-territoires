module.exports = {};
const { Permission } = require("./permission");
const { GraphQLObjectType, GraphQLString, GraphQLList } = require("graphql");

const Role = new GraphQLObjectType({
  name: "role",
  fields: {
    id: { type: GraphQLString },
    label: { type: GraphQLString },
    permissions: {
      type: new GraphQLList(Permission)
    }
  }
});
Object.assign(module.exports, { Role });
