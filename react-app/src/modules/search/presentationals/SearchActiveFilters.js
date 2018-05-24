import React from "react";
import Chip from "material-ui/Chip";
import { blue300 } from "material-ui/styles/colors";
import PropTypes from "prop-types";
import { getLabelFromEnumValue, getEnumName } from "modules/enums";
import FlatButton from "material-ui/FlatButton";

const styles = {
  chip: {
    margin: 4
  },
  wrapper: {
    display: "flex",
    flexWrap: "wrap"
  }
};

function filtersAreEmpty(filters) {
  const values = Object.keys(filters).filter(
    filterId => filters[filterId] && filters[filterId].length > 0
  );
  if (values.length === 0) {
    return true;
  }
  return false;
}

const DeleteAllFilters = ({ onRequestReset }) => (
  <FlatButton
    primary={true}
    style={{ marginRight: "20px" }}
    label="Effacer les filtres"
    onClick={onRequestReset}
  />
);

const ChipFilter = ({ filterId, filterValue, onRequestDelete }) => (
  <Chip
    key={`${filterId} - ${filterValue}`}
    style={styles.chip}
    backgroundColor={blue300}
    onRequestDelete={() => onRequestDelete(filterId, filterValue)}
  >
    <em>{getEnumName("aide", filterId)}</em> :{" "}
    {getLabelFromEnumValue("aide", filterId, filterValue)}
  </Chip>
);

const StickyActiveStyles = () => (
  <style>
    {
      ".sticky-outer-wrapper.active .sticky-inner-wrapper {box-shadow: 0px 0px 40px 0px rgba(0, 0, 0, 0.3);}"
    }
  </style>
);

const SearchActiveFilters = ({ filters, onRequestDelete, onRequestReset }) => {
  if (filtersAreEmpty(filters)) return null;
  return (
    <div style={styles.wrapper}>
      <StickyActiveStyles />
      <DeleteAllFilters onRequestReset={onRequestReset} />
      {Object.keys(filters).map(filterId => {
        return (
          filters[filterId] && (
            <span key={filterId} style={styles.wrapper}>
              {filters[filterId].map(filterValue => (
                <ChipFilter
                  key={filterId + "-" + filterValue}
                  filterId={filterId}
                  filterValue={filterValue}
                  onRequestDelete={onRequestDelete}
                />
              ))}
            </span>
          )
        );
      })}
    </div>
  );
};

SearchActiveFilters.propTypes = {
  // {type:["autre","financement"],etape:["pre_operationnel"]}
  filters: PropTypes.object,
  onRequestDelete: PropTypes.func.isRequired,
  onRequestReset: PropTypes.func
};

export default SearchActiveFilters;
