import React from "react";
import AdminLayout from "modules/admin/layouts/AdminLayout";
import AideForm from "modules/admin/forms/AideForm";

class AideFormPage extends React.Component {
  render() {
    return (
      <AdminLayout>
        <h1 className="title is-1">Créer une aide</h1>
        <AideForm operation={"creation"} />
      </AdminLayout>
    );
  }
}

export default AideFormPage;
