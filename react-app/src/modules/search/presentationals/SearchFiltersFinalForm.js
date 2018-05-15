import React from "react";
import { Form, Field } from "react-final-form";
import { FormSpy } from "react-final-form";
import propTypes from "prop-types";
import classnames from "classnames";
import SlideDown from "modules/ui-kit/reactSpring/SlideDown";
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
class SearchFilters extends React.Component {
  state = {
    activeFilters: {
      type: true,
      etape: false
    }
  };
  static propTypes = {
    // si une aide est passée en props, on considèrera
    // qu'on est en mode édition
    aide: propTypes.object,
    onFiltersChange: propTypes.func
  };
  handleSubmit = values => {};
  handleFormChange = values => {
    this.props.onFiltersChange(values);
  };
  handleClickLabel = id => {
    this.setState(prevState => {});
  };
  render() {
    return (
      <div className="SearchFilters">
        {JSON.stringify(this.state, 0, 2)}
        <Form
          onSubmit={this.handleSubmit}
          validate={validate}
          render={({
            handleSubmit,
            submitting,
            pristine,
            values,
            errors,
            form
          }) => (
            <form onSubmit={handleSubmit}>
              {/* listen for form values change from outside of the <form> tag */}
              <FormSpy
                subscription={{ values: true }}
                onChange={this.handleFormChange}
              />
              {/* ================== */}
              <div className="field">
                <label
                  className="label"
                  onClick={() => this.handleClickLabel("type")}
                >
                  {" "}
                  Type d'aide{" "}
                </label>
                <SlideDown show={this.state.activeFilters.type}>
                  {TYPE_OPTIONS.map(option => {
                    return (
                      <div key={option.value}>
                        <label className="checkbox">
                          <Field
                            name="type"
                            component="input"
                            type="checkbox"
                            value={option.value}
                          />{" "}
                          {option.label}
                        </label>
                      </div>
                    );
                  })}
                </SlideDown>
              </div>
              {/* ================== */}
              <div className="field">
                <label
                  className={classnames("label")}
                  onClick={() => this.handleClickLabel("etape")}
                >
                  Quand mobiliser l'aide
                </label>
                {ETAPE_OPTIONS.map(option => {
                  return (
                    <div key={option.value}>
                      <label className="checkbox">
                        <Field
                          name="etape"
                          component="input"
                          type="checkbox"
                          value={option.value}
                        />{" "}
                        {option.label}
                      </label>
                    </div>
                  );
                })}
              </div>
              {/* ================== */}
              <div className="field">
                <label
                  className={classnames("label")}
                  onClick={() => this.handleClickLabel("formeDeDiffusion")}
                >
                  Modalité de diffusion
                </label>
                {FORME_DE_DIFFUSION_OPTIONS.map(option => {
                  return (
                    <div key={option.value}>
                      <label className="checkbox">
                        <Field
                          name="formeDeDiffusion"
                          component="input"
                          type="checkbox"
                          value={option.value}
                        />{" "}
                        {option.label}
                      </label>
                    </div>
                  );
                })}
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
                {DESTINATION_OPTIONS.map(option => {
                  return (
                    <div key={option.value}>
                      <label className="checkbox">
                        <Field
                          name="destination"
                          component="input"
                          type="checkbox"
                          value={option.value}
                        />{" "}
                        {option.label}
                      </label>
                    </div>
                  );
                })}
              </div>
              {/* ================== */}
              <div className="field">
                <label
                  className={classnames("label")}
                  onClick={() => this.handleClickLabel("thematiques")}
                >
                  {" "}
                  Thématiques{" "}
                </label>
                {THEMATIQUES_OPTIONS.map(option => {
                  return (
                    <div key={option.value}>
                      <label className="checkbox">
                        <Field
                          name="thematiques"
                          component="input"
                          type="checkbox"
                          value={option.value}
                        />{" "}
                        {option.label}
                      </label>
                    </div>
                  );
                })}
              </div>
              {/* ================== */}
            </form>
          )}
        />
      </div>
    );
  }
}

export default SearchFilters;
