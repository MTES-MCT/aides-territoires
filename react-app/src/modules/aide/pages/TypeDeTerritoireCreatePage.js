import React from "react";
import AdminLayout from "modules/admin/layouts/AdminLayout";
import TypeDeTerritoireFormContainer from "modules/aide/decorators/TypeDeTerritoireFormContainer";

class TypeDeTerritoireFormPage extends React.Component {
  render() {
    return (
      <AdminLayout>
        <h1 className="title is-1">Créer un type de territoire</h1>
        <TypeDeTerritoireFormContainer />
      </AdminLayout>
    );
  }
}

export default TypeDeTerritoireFormPage;
