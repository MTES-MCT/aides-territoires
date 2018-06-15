const permissions = [
  {
    id: "create_aide",
    label: "Créer une aide"
  },
  {
    id: "edit_any_aide",
    label: "Créer une aide"
  },
  {
    id: "delete_any_aide",
    label: "Supprimer un aide"
  },
  {
    id: "delete_own_aide",
    label: "Supprimer un aide"
  },
  {
    id: "edit_own_aide",
    label: "Supprimer un aide"
  }
];

const roles = [
  {
    roleId: "admin",
    roleName: "Administrataeur",
    permissions: ["create_aide", "delete_any_aide", "edit_any_aide"]
  },
  {
    roleId: "contributeur",
    roleName: "Contributeur",
    permissions: ["create_aide", "delete_own_aide", "edit_own_aide"]
  }
];

export { roles, permissions };
