import React from "react";
import { connect } from "react-redux";
import Chip from "material-ui/Chip";
import { blue300, indigo900 } from "material-ui/styles/colors";

const styles = {
  chip: {
    margin: 4
  },
  wrapper: {
    display: "flex",
    flexWrap: "wrap"
  }
};

const handleRequestDelete = () => {};
const handleClick = () => {};

const ActiveFilters = ({ filters }) => {
  return (
    <div>
      {Object.keys(filters).map(filterId => {
        return (
          <div>
            <div style={styles.wrapper}>
              <Chip backgroundColor={"white"} style={styles.chip}>
                <strong>{filterId} </strong>
              </Chip>
              {filters[filterId].map(filter => {
                return (
                  <Chip
                    style={styles.chip}
                    onRequestDelete={handleRequestDelete}
                    onClick={handleClick}
                    backgroundColor={blue300}
                  >
                    {filter}
                  </Chip>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default connect(state => {
  if (state.form.searchFilters && state.form.searchFilters.values) {
    console.log(state.form.searchFilters.values);
    return { filters: state.form.searchFilters.values };
  }
  return { filters: {} };
})(ActiveFilters);
