import React from "react";
import AdminLayout from "../layouts/AdminLayout";
import AdminAideForm from "../admin/AdminAideForm";

class AideFormPage extends React.Component {
  render() {
    return (
      <AdminLayout>
        <h1 className="title is-1">Créer une aide</h1>
        <AdminAideForm operation={"creation"} />
      </AdminLayout>
    );
  }
}

export default AideFormPage;
