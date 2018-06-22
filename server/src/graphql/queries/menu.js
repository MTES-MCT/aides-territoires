const { GraphQLString, GraphQLObjectType, GraphQLList } = require("graphql");
const { getAllMenus, getMenuById } = require("../../config/menus");

const MenuLinkType = new GraphQLObjectType({
  name: "menuLink",
  fields: {
    href: { type: GraphQLString },
    title: { type: GraphQLString }
  }
});

const MenuType = new GraphQLObjectType({
  name: "menu",
  fields: {
    id: { type: GraphQLString },
    label: { type: GraphQLString },
    links: { type: new GraphQLList(MenuLinkType) }
  }
});

// a simple query to test our graphql API
module.exports = {
  allMenus: {
    type: new GraphQLList(MenuType),
    resolve: (_, args, context) => {
      return getAllMenus(context.user);
    }
  },
  menu: {
    type: MenuType,
    args: {
      id: {
        type: GraphQLString
      }
    },
    resolve: (_, { id }, { user }) => {
      return getMenuById(id, user);
    }
  }
};
