import React from "react";
import Chip from "material-ui/Chip";
import { blue300 } from "material-ui/styles/colors";
import PropTypes from "prop-types";

const styles = {
  chip: {
    margin: 4
  },
  wrapper: {
    display: "flex",
    flexWrap: "wrap"
  }
};

const SearchActiveFilters = ({ filters, onRequestDelete }) => {
  console.log(filters);
  return (
    <div style={styles.wrapper}>
      {Object.keys(filters).map(filterId => {
        console.log(filters);
        return (
          filters[filterId].length > 0 && (
            <span key={filterId} style={styles.wrapper}>
              {filters[filterId].map(filter => {
                return (
                  <Chip
                    key={`${filterId} - ${filter}`}
                    style={styles.chip}
                    backgroundColor={blue300}
                    onRequestDelete={event => onRequestDelete(filterId, filter)}
                  >
                    <em>{filterId}</em> : {filter}
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
  onRequestDelete: PropTypes.func.isRequired
};

export default SearchActiveFilters;
