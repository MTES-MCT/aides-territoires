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
    const aides = this.props.aides.map(aide => ({ ...aide }));
    return (
      <div>
        <Transition
          native
          keys={aides.map(aide => aide.id)}
          from={{ opacity: 0, height: 0 }}
          enter={{ opacity: 1, height: 20 }}
          leave={{ opacity: 0, height: 0 }}
        >
          {aides.map(aide => styles => (
            <animated.div
              className={this.props.classes.listItem}
              style={{ styles }}
            >
              <AideListItem aide={aide} />
            </animated.div>
          ))}
        </Transition>
      </div>
    );
  }
}

export default injectSheet(styles)(SearchResultList);
