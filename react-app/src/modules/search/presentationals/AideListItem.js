import React from "react";
import PropTypes from "prop-types";
import AideListItemDetails from "./AideListItemDetails";
import RaisedButton from "material-ui/RaisedButton";
import { Spring, animated } from "react-spring";
import { getLabelFromEnumValue } from "modules/enums";
import injectSheet from "react-jss";

const styles = {
  wrapper: {
    paddingTop: "2rem"
  },
  showMoreButton: {
    marginTop: "1rem",
    textAlign: "center"
  }
};

const DESCRIPTION_CHARS_LIMIT = 300;

class AideListItem extends React.Component {
  state = {
    showDetails: false
  };
  static propTypes = {
    aide: PropTypes.object.isRequired,
    label: PropTypes.string
  };
  handleMoreButtonClick = () => {
    this.setState(prevState => ({
      showDetails: !prevState.showDetails
    }));
  };
  render() {
    const { aide } = this.props;
    return (
      <div
        style={{ position: "relative" }}
        className={`box ${this.props.classes.wrapper}`}
      >
        <h2 className="title is-4">{aide.nom}</h2>
        <div className="tag" style={{ position: "absolute", top: 0, left: 0 }}>
          {getLabelFromEnumValue(
            "aide",
            "perimetreApplicationType",
            aide.perimetreApplicationType
          )}
        </div>
        <p className="description">
          {aide.description.substring(0, DESCRIPTION_CHARS_LIMIT)}
          {!this.state.showDetails &&
            aide.description.length > DESCRIPTION_CHARS_LIMIT &&
            "..."}
          {this.state.showDetails &&
            aide.description.substring(DESCRIPTION_CHARS_LIMIT)}
        </p>
        <Spring
          native
          from={{ maxHeight: 0, overflow: "hidden" }}
          to={{
            maxHeight: this.state.showDetails ? 500 : 0
          }}
        >
          {styles => (
            <animated.div style={styles}>
              <AideListItemDetails aide={aide} />
            </animated.div>
          )}
        </Spring>

        <div className={this.props.classes.showMoreButton}>
          <RaisedButton
            onClick={this.handleMoreButtonClick}
            style={{ marginRight: "20px" }}
            primary={true}
            label={!this.state.showDetails ? "Voir plus" : "cacher les détails"}
          />
        </div>
      </div>
    );
  }
}

export default injectSheet(styles)(AideListItem);
