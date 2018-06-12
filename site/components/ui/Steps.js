import React from "react";
import injectSheet from "react-jss";
import PropTypes from "prop-types";
import Container from "../ui/Container";
import uiConfig from "../../ui.config";

const StepType = PropTypes.shape({
  title: PropTypes.string.isRequired,
  description: PropTypes.string
});

let Steps = ({ classes, children, steps }) => {
  return (
    <div className={classes.root}>
      {steps.map((step, index) => {
        return (
          <div className={classes.step}>
            <StepItem key={step.title} number={index + 1} step={step} />
          </div>
        );
      })}
    </div>
  );
};
Steps.propTypes = {
  steps: PropTypes.arrayOf(StepType)
};
Steps = injectSheet({
  root: {
    width: "900px",
    display: "flex",
    margin: "auto",
    justifyContent: "space-between"
  },
  [uiConfig.breakpoints.smallScreen]: {
    root: {
      display: "block",
      textAlign: "center",
      margin: "auto",
      width: "100%"
    },
    step: {}
  }
})(Steps);

let StepItem = ({ step, number, classes }) => {
  return (
    <div className={classes.root}>
      <div className={classes.number}>{number}</div>
      <h4 className={classes.title}>{step.title}</h4>
      <p className={classes.description}>{step.description}</p>
    </div>
  );
};
StepItem.propTypes = {
  step: StepType
};
StepItem = injectSheet({
  root: {
    textAlign: "center",
    margin: "auto",
    width: "280px"
  },
  number: {
    border: "solid black 1px",
    fontWeight: "100",
    paddingTop: "5px",
    fontSize: "30px",
    width: "50px",
    height: "45px",
    margin: "auto"
  },
  [uiConfig.breakpoints.smallScreen]: {
    root: {
      paddingTop: "3rem"
    },
    step: {}
  }
})(StepItem);

export default Steps;
