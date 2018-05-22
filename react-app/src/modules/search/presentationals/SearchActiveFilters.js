import React from "react";
import Chip from "material-ui/Chip";
import { blue300 } from "material-ui/styles/colors";

const styles = {
  chip: {
    margin: 4
  },
  wrapper: {
    display: "flex",
    flexWrap: "wrap"
  }
};

const SearchActiveFilters = ({ filters }) => {
  return (
    <div style={styles.wrapper}>
      {Object.keys(filters).map(filterId => {
        return (
          filters[filterId].length > 0 && (
            <span key={filterId} style={styles.wrapper}>
              {filters[filterId].map(filter => {
                return (
                  <Chip
                    key={filters[filterId]}
                    style={styles.chip}
                    backgroundColor={blue300}
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

export default SearchActiveFilters;
