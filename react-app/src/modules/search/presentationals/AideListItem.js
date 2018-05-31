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
import EuroIcon from "material-ui/svg-icons/action/euro-symbol";
import SettingsIcon from "material-ui/svg-icons/action/settings";

const styles = {
  root: {
    paddingBottom: "2.5rem",
    position: "relative"
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
  structurePorteuse: {
    textTransform: "uppercase",
    color: "gray",
    fontSize: "25px",
    fontWeight: "bold"
  },
  perimetre: {
    textTransform: "uppercase",
    color: "gray",
    fontSize: "21px",
    fontWeight: "normal"
  },
  icons: {
    position: "absolute",
    right: "0"
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

const AAP = () => (
  <div
    style={{
      padding: "0.5rem",
      background: "red",
      color: "white",
      textAlign: "center"
    }}
  >
    AAP
  </div>
);

const IconRound = ({ children, top = "8px", left = "0", title }) => {
  return (
    <div
      title={title}
      style={{
        border: "solid silver 1px",
        background: "white",
        borderRadius: "1000px",
        width: "43px",
        height: "43px",
        textAlign: "center"
      }}
    >
      <span style={{ position: "relative", top, left }}>{children}</span>
    </div>
  );
};

const IconsBarItem = ({ children }) => (
  <div style={{ marginLeft: "0.5rem" }}>{children}</div>
);

const IconsBar = ({ aide }) => {
  const itemStyle = {
    margin: "1rem"
  };
  return (
    <div style={{ display: "flex" }}>
      <IconsBarItem>
        {aide.type === "financement" ? (
          <IconRound title="Aide financière" left="-2px">
            <EuroIcon />
          </IconRound>
        ) : (
          <IconRound title="Aide non financière">
            <SettingsIcon />
          </IconRound>
        )}
      </IconsBarItem>
      <IconsBarItem>
        {aide.categorieParticuliere.includes("AAP") && <AAP />}
      </IconsBarItem>
    </div>
  );
};

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
        <div className={classes.icons}>
          <IconsBar aide={aide} />
        </div>
        <div className={classes.structurePorteuse}>
          {aide.structurePorteuse}
          <span className={classes.perimetre}>
            {" - "}
            {getLabelFromEnumValue(
              "aide",
              "perimetreApplicationType",
              aide.perimetreApplicationType
            )}
          </span>
        </div>
        {/*<EuroIcon />*/}
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
        {aide.dateEcheance && <DateEcheance date={aide.dateEcheance} />}
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
