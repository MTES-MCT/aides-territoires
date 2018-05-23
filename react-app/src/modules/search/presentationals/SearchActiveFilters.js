import React from "react";
import Chip from "material-ui/Chip";
import { blue300 } from "material-ui/styles/colors";
import PropTypes from "prop-types";
import { getLabelFromEnumId } from "modules/aide/enums";
import RaisedButton from "material-ui/RaisedButton";

const styles = {
  chip: {
    margin: 4
  },
  wrapper: {
    display: "flex",
    flexWrap: "wrap"
  }
};

const SearchActiveFilters = ({ filters, onRequestDelete, onRequestReset }) => {
  const values = Object.keys(filters).filter(
    filterId => filters[filterId].length > 0
  );
  if (values.length === 0) {
    return null;
  }
  return (
    <div style={styles.wrapper}>
      <RaisedButton
        style={{ marginRight: "20px" }}
        label="Reset"
        onClick={onRequestReset}
      />
      {Object.keys(filters).map(filterId => {
        return (
          filters[filterId].length > 0 && (
            <span key={filterId} style={styles.wrapper}>
              {filters[filterId].map(filterValue => {
                return (
                  <Chip
                    key={`${filterId} - ${filterValue}`}
                    style={styles.chip}
                    backgroundColor={blue300}
                    onRequestDelete={() =>
                      onRequestDelete(filterId, filterValue)
                    }
                  >
                    <em>{filterId}</em> :{" "}
                    {getLabelFromEnumId(filterId, filterValue)}
                  </Chip>
                );
              })}
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
