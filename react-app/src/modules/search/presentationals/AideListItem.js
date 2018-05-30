import React from "react";
import PropTypes from "prop-types";
import AideListItemDetails from "./AideListItemDetails";
import RaisedButton from "material-ui/RaisedButton";
import { Spring, animated } from "react-spring";
import { getLabelFromEnumValue } from "modules/enums";
import injectSheet from "react-jss";
import classnames from "classnames";
import { blue300 } from "material-ui/styles/colors";
import moment from "moment";
import CalendarIcon from "material-ui/svg-icons/action/event";

const styles = {
  root: {
    paddingBottom: "2.5rem"
  },
  showMoreButton: {
    "&:hover": {
      color: "white"
    },
    marginTop: "1rem",
    textAlign: "center",
    background: blue300,
    color: "white"
  },
  perimetre: {
    fontWeight: "bold",
    textTransform: "uppercase",
    fontSize: "25px",
    color: "gray"
  },
  title: {
    fontWeight: "bold",
    textTransform: "uppercase",
    fontSize: "25px"
  },
  titleUnderline: {
    borderBottom: `solid ${blue300} 2px`,
    maxWidth: "200px"
  },
  description: {
    paddingTop: "1rem",
    color: "#555"
  }
};

const DESCRIPTION_CHARS_LIMIT = 300;

const DateEcheance = ({ date }) => (
  <div style={{ paddingTop: "1rem" }}>
    <span
      style={{
        paddingRight: "5px",
        position: "relative",
        top: "5px",
        display: "inline-block"
      }}
    >
      <CalendarIcon />
    </span>
    <span>Échéance le {moment(date).format("DD/MM/YYYY")}</span>
  </div>
);

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
    const { aide, classes } = this.props;
    return (
      <div className={this.props.classes.root}>
        <div className={classes.perimetre}>
          [{getLabelFromEnumValue(
            "aide",
            "perimetreApplicationType",
            aide.perimetreApplicationType
          )}]
        </div>
        <h2 className={classes.title}>{aide.nom}</h2>
        <div className={classes.titleUnderline} />
        {aide.description.trim().length > 0 && (
          <p className={classes.description}>
            {aide.description.substring(0, DESCRIPTION_CHARS_LIMIT)}
            {!this.state.showDetails &&
              aide.description.length > DESCRIPTION_CHARS_LIMIT &&
              "..."}
            {this.state.showDetails &&
              aide.description.substring(DESCRIPTION_CHARS_LIMIT)}
          </p>
        )}
        {aide.dateEcheance && <DateEcheance data={aide.dateEcheance} />}
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

        <div
          className={classnames("button", classes.showMoreButton)}
          onClick={this.handleMoreButtonClick}
        >
          {!this.state.showDetails ? "Voir plus" : "cacher les détails"}
        </div>
      </div>
    );
  }
}

export default injectSheet(styles)(AideListItem);
