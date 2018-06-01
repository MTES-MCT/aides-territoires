import React from "react";
import Chip from "material-ui/Chip";
import { blue300 } from "material-ui/styles/colors";
import PropTypes from "prop-types";
import { getLabelFromEnumValue, getEnumName } from "modules/enums";
import FlatButton from "material-ui/FlatButton";
import injectSheet from "react-jss";
import { connect } from "react-redux";
import { change, reset } from "redux-form";

/**
 * Bouton pour effacer tous les filtres
 */
const DeleteAllFilters = ({ classes, onClick }) => (
  <FlatButton
    primary={true}
    style={{ marginRight: "20px" }}
    label="Effacer les filtres"
    onClick={onClick}
  />
);

/**
 * Affiche tous les filtres actifs
 * @param {*} param0
 */
let SearchActiveFilters = class extends React.Component {
  static propTypes = {
    // {type:["autre","financement"],etape:["pre_operationnel"]}
    filters: PropTypes.object
  };
  /**
   * Désactivé le filtre cliqué
   * @param {string} fieldId
   * @param {string} filterValue
   */
  handleRequestDeleteCheckbox = (fieldId, filterValue) => {
    const currentFilters = this.props.filters;
    if (currentFilters[fieldId]) {
      let newFilterValue = currentFilters[fieldId].filter(value => {
        return value !== filterValue;
      });
      if (newFilterValue.length === 0) {
        newFilterValue = null;
      }
      this.props.change("searchFilters", fieldId, newFilterValue);
    }
  };
  handleRequestDelete = (fieldId, filterValue) => {
    const currentFilters = this.props.filters;
    if (currentFilters[fieldId]) {
      let newFilterValue = currentFilters[fieldId].filter(value => {
        return value !== filterValue;
      });
      if (newFilterValue.length === 0) {
        newFilterValue = null;
      }
      this.props.change("searchFilters", fieldId, newFilterValue);
    }
  };
  /**
   * Remettre à zéro tous les filtres activés par l'utilisateur
   */
  handleDeleteAllClick = () => {
    // remet à zéro le formulaire des filtres de recherche via le store
    this.props.reset();
  };
  render() {
    const { classes, filters, onRequestDelete, onRequestReset } = this.props;
    return (
      <div className={classes.root}>
        <DeleteAllFilters onClick={this.handleDeleteAllClick} />
        <span className={classes.chips}>
          {Object.keys(filters).map(filterId => {
            if (!filters[filterId]) return null;
            /*
            if (typeof filters[filterId] === "string") {
              <ChipFilterString
                key={filterId}
                filterId={filterId}
                label={filters[filterId]}
                onRequestDelete={this.handleRequestDelete}
              />;
            }
            */
            // affichage des filtres pour les checboxs, une Chip par valeur
            if (filters[filterId].constructor === Array) {
              {
                return filters[filterId].map(filterValue => (
                  <Chip
                    key={filterId + "-" + filterValue}
                    style={{ margin: 4 }}
                    backgroundColor={blue300}
                    onRequestDelete={() =>
                      this.handleRequestDeleteCheckbox(filterId, filterValue)
                    }
                  >
                    <em>{getEnumName("aide", filterId)}</em> :{" "}
                    {getLabelFromEnumValue("aide", filterId, filterValue)}
                  </Chip>
                ));
              }
            }
          })}
        </span>
      </div>
    );
  }
};
SearchActiveFilters = injectSheet({
  root: {
    display: "flex"
  },
  chips: {
    display: "flex",
    flexWrap: "wrap"
  }
})(SearchActiveFilters);

function mapStateToProps(state) {
  if (state.form.searchFilters && state.form.searchFilters.values) {
    return {
      // les filtres sélectionnés par l'utilisateur pour sa recherche
      // ainsi que les données de périmètre qui ont été enregistré
      // par le moteur de recherche pas territoire
      filters: state.form.searchFilters.values
    };
  }
  // éviter une erreur pour cause de filters undefined
  return { filters: {} };
}

function mapDispatchToProps(dispatch) {
  return {
    change: (form, field, value) => {
      dispatch(change(form, field, value));
    },
    reset: () => dispatch(reset("searchFilters"))
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(
  SearchActiveFilters
);
