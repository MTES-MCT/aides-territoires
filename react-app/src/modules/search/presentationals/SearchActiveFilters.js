import React from "react";
import Chip from "material-ui/Chip";
import { blue300 } from "material-ui/styles/colors";
import PropTypes from "prop-types";
import { getLabelFromEnum } from "modules/aide/enums";

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
  return (
    <div style={styles.wrapper}>
      {Object.keys(filters).map(filterId => {
        return (
          filters[filterId].length > 0 && (
            <span key={filterId} style={styles.wrapper}>
              {filters[filterId].map(filterValue => {
                console.log(filterValue);
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
                    {getLabelFromEnum(filterId, filterValue)}
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
