const { userHasPermission, userHasRole } = require("../services/user");

function getAdminMenu(user) {
  const links = [];
  links.push({
    href: "/admin/aide/create",
    title: "Créer une aide"
  });
  links.push({
    href: "/admin/aide/list",
    title: "List des aides"
  });
  if (userHasPermission(user, "see_permissions_overview")) {
    links.push({
      href: "/admin/aide/permissions",
      title: "Permissions et rôles"
    });
  }
  const menu = {
    id: "adminMenu",
    label: "Menu d'administration",
    links
  };
  return menu;
}

function getAllMenus(user) {
  const allMenus = [];
  if (userHasRole(user, "admin") || userHasRole(user, "contributeur")) {
    allMenus.push(getAdminMenu(user));
  }
  return allMenus;
}

function getMenuById(id, user) {
  const allMenus = getAllMenus(user);
  return allMenus.find(menu => menu.id === id);
}

module.exports = { getAllMenus, getMenuById };
