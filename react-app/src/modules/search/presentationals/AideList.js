import React from "react";
import PropTypes from "prop-types";
import AideListItem from "./AideListItem";
import { Transition, animated } from "react-spring";
import injectSheet from "react-jss";

const styles = {
  listItem: {
    marginBottom: "1rem"
  }
};

class SearchResultList extends React.Component {
  static propTypes = {
    aides: PropTypes.array.isRequired,
    title: PropTypes.string
  };
  render() {
    // clone aides object or transition won't work
    // because it needs an extensible object
    // const aides = this.props.aides.map(aide => ({ ...aide }));
    return (
      <div style={{ padding: "0.5rem" }}>
        {this.props.aides.map(aide => (
          <AideListItem key={aide.id} aide={aide} />
        ))}
      </div>
    );
  }
}

export default injectSheet(styles)(SearchResultList);
