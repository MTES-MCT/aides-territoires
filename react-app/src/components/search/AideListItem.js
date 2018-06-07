import React from "react";
import PropTypes from "prop-types";
import AideListItemDetails from "./AideListItemDetails";
import SlideDown from "../ui/reactSpring/SlideDown";
import { getLabelFromEnumValue } from "../../enums";
import injectSheet from "react-jss";
import classnames from "classnames";
import { blue300 } from "material-ui/styles/colors";
import moment from "moment";
import CalendarIcon from "material-ui/svg-icons/action/event";
import EuroIcon from "material-ui/svg-icons/action/euro-symbol";
import SettingsIcon from "material-ui/svg-icons/action/settings";

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
    const { aide, classes } = this.props;
    return (
      <div className={this.props.classes.root}>
        <div className={classes.iconsBar}>
          <AideIconsBar aide={aide} />
        </div>
        <div className={classes.structurePorteuse}>
          {aide.structurePorteuse} {" - "}
          <AidePerimetre aide={aide} />
        </div>
        <h2 className={classes.title}>{aide.nom}</h2>
        <AideTitleUnderline aide={aide} />
        {aide.description.trim().length > 0 && (
          <AideDescription aide={aide} showDetails={this.state.showDetails} />
        )}
        {aide.dateEcheance && <AideDateEcheance date={aide.dateEcheance} />}

        <SlideDown show={this.state.showDetails}>
          <AideListItemDetails aide={aide} />
        </SlideDown>

        <AideShowMoreButton
          showDetails={this.state.showDetails}
          onClick={this.handleMoreButtonClick}
        />
      </div>
    );
  }
}
AideListItem = injectSheet({
  root: {
    paddingBottom: "2.5rem",
    position: "relative"
  },
  structurePorteuse: {
    textTransform: "uppercase",
    color: "gray",
    fontSize: "25px",
    fontWeight: "bold"
  },
  iconsBar: {
    position: "absolute",
    right: "0"
  },
  title: {
    fontWeight: "bold",
    textTransform: "uppercase",
    fontSize: "25px"
  }
})(AideListItem);

const AideTitleUnderline = ({ aide }) => (
  <div
    style={{
      borderBottom: `solid ${blue300} 2px`,
      maxWidth: "200px"
    }}
  />
);

/**
 * AidePerimetre
 */
let AidePerimetre = ({ classes, aide }) => (
  <span className={classes.root}>
    {getLabelFromEnumValue(
      "aide",
      "perimetreApplicationType",
      aide.perimetreApplicationType
    )}{" "}
    {aide.perimetreApplicationNom}
  </span>
);
AidePerimetre = injectSheet({
  root: {
    textTransform: "uppercase",
    color: "gray",
    fontSize: "21px",
    fontWeight: "normal"
  }
})(AidePerimetre);

/**
 * AideShowMoreButton
 */
let AideShowMoreButton = ({ showDetails, classes, onClick }) => (
  <div className={classnames("button", classes.root)} onClick={onClick}>
    {!showDetails ? "Voir plus" : "cacher les détails"}
  </div>
);
AideShowMoreButton = injectSheet({
  root: {
    "&:hover": {
      color: "white"
    },
    marginTop: "1rem",
    textAlign: "center",
    background: blue300,
    color: "white"
  }
})(AideShowMoreButton);

/**
 * AideDescription
 */
let AideDescription = ({ aide, classes, showDetails = false }) => (
  <div className={classes.root}>
    {aide.description.substring(0, DESCRIPTION_CHARS_LIMIT)}
    {!showDetails && aide.description.length > DESCRIPTION_CHARS_LIMIT && "..."}
    {showDetails && aide.description.substring(DESCRIPTION_CHARS_LIMIT)}
  </div>
);
AideDescription = injectSheet({
  root: {
    paddingTop: "1rem",
    color: "#555"
  }
})(AideDescription);

/**
 * AideDateEcheance
 */
let AideDateEcheance = ({ date, classes }) => (
  <div style={{ paddingTop: "1rem" }}>
    <span className={classes.iconWrapper}>
      <CalendarIcon />
    </span>
    <span>Échéance le {moment(date).format("DD/MM/YYYY")}</span>
  </div>
);
AideDateEcheance = injectSheet({
  root: {
    paddingTop: "1rem"
  },
  iconWrapper: {
    paddingRight: "5px",
    position: "relative",
    top: "5px",
    display: "inline-block"
  }
})(AideDateEcheance);

/**
 * APP
 */
let AAP = ({ classes }) => <div className={classes.root}>AAP</div>;
AAP = injectSheet({
  root: {
    padding: "0.5rem",
    background: "red",
    color: "white",
    textAlign: "center"
  }
})(AAP);

/**
 * IconRound
 */
let IconRound = ({ classes, title, children }) => (
  <div title={title} className={classes.root}>
    <span className={classes.span}>{children}</span>
  </div>
);
IconRound = injectSheet({
  root: {
    border: "solid silver 1px",
    background: "white",
    borderRadius: "1000px",
    width: "43px",
    height: "43px",
    textAlign: "center"
  },
  span: ({ top = "7px", left = "0" }) => {
    return {
      position: "relative",
      top,
      left
    };
  }
})(IconRound);

/**
 * AideIconsBarItem
 */
const AideIconsBarItem = ({ children }) => (
  <div style={{ marginLeft: "0.5rem" }}>{children}</div>
);

/**
 * AideIconsBar
 */
const AideIconsBar = ({ aide }) => {
  return (
    <div style={{ display: "flex" }}>
      <AideIconsBarItem>
        {aide.type === "financement" ? (
          <IconRound title="Aide financière" left="-2px">
            <EuroIcon />
          </IconRound>
        ) : (
          <IconRound title="Aide non financière">
            <SettingsIcon />
          </IconRound>
        )}
      </AideIconsBarItem>
      <AideIconsBarItem>
        {aide.categorieParticuliere.includes("AAP") && <AAP />}
      </AideIconsBarItem>
    </div>
  );
};

export default AideListItem;
