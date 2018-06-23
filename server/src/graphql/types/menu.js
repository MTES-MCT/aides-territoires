module.exports = {};
const { GraphQLObjectType, GraphQLString, GraphQLList } = require("graphql");

const MenuLink = new GraphQLObjectType({
  name: "menuLink",
  fields: {
    href: { type: GraphQLString },
    title: { type: GraphQLString }
  }
});

const Menu = new GraphQLObjectType({
  name: "menu",
  fields: {
    id: { type: GraphQLString },
    label: { type: GraphQLString },
    links: { type: new GraphQLList(MenuLink) }
  }
});

Object.assign(module.exports, { Menu, MenuLink });
