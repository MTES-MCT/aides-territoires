import React from "react";
import { Field, reduxForm } from "redux-form";
import Store from "store";
import propTypes from "prop-types";
import classnames from "classnames";
import SlideDown from "modules/ui-kit/reactSpring/SlideDown";
import CheckboxGroup from "modules/ui-kit/reduxForm/CheckboxGroup";
import { connect } from "react-redux";
import {
  PERIMETRE_APPLICATION_OPTIONS,
  PERIMETRE_DIFFUSION_OPTIONS,
  TYPE_OPTIONS,
  ETAPE_OPTIONS,
  FORME_DE_DIFFUSION_OPTIONS,
  BENEFICIAIRES_OPTIONS,
  DESTINATION_OPTIONS,
  THEMATIQUES_OPTIONS,
  STATUS_OPTIONS,
  STATUS_PUBLICATION_OPTIONS
} from "modules/aide/enums";
import "./SearchFilter.css";

const validate = values => {
  const errors = {};
  if (!values.nom || values.nom.trim().length === 0) {
    errors.nom = "Le champ nom est requis";
  }
  return errors;
};

let SearchFilters = props => {
  const { handleSubmit, formValues, pristine, reset, submitting } = props;
  return (
    <form className="SearchFilters">
      {/* ================== */}
      <div className="field">
        <label className="label" onClick={() => this.handleClickLabel("type")}>
          Type d'aide
        </label>
        <CheckboxGroup name="type" options={TYPE_OPTIONS} />
      </div>
      {/* ================== */}
      <div className="field">
        <label
          className={classnames("label")}
          onClick={() => this.handleClickLabel("etape")}
        >
          Quand mobiliser l'aide
        </label>
        <CheckboxGroup name="etape" options={ETAPE_OPTIONS} />
      </div>
      {/* ================== */}
      <div className="field">
        <label
          className={classnames("label")}
          onClick={() => this.handleClickLabel("formeDeDiffusion")}
        >
          Modalité de diffusion
        </label>
        <CheckboxGroup
          name="formeDeDiffusion"
          options={FORME_DE_DIFFUSION_OPTIONS}
        />
      </div>
      {/* ================== */}
      <div className="field">
        <label
          className={classnames("label")}
          onClick={() => this.handleClickLabel("destination")}
        >
          {" "}
          Destination de l'aide{" "}
        </label>
        <CheckboxGroup name="destination" options={DESTINATION_OPTIONS} />
      </div>
      {/* ================== */}
      <div className="field">
        <label
          className={classnames("label")}
          onClick={() => this.handleClickLabel("thematiques")}
        >
          Thématiques
        </label>
        <CheckboxGroup name="thematiques" options={THEMATIQUES_OPTIONS} />
      </div>
      {/* ================== */}
    </form>
  );
};

SearchFilters = reduxForm({
  // a unique name for the form
  form: "searchFilters"
})(SearchFilters);

SearchFilters = connect(state => {
  return {
    formValues: state.form.searchFilters ? state.form.searchFilters.values : {}
  };
})(SearchFilters);

export default SearchFilters;
