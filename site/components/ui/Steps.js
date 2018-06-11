import React from "react";
import injectSheet from "react-jss";
import PropTypes from "prop-types";
import Container from "../ui/Container";

const StepType = PropTypes.shape({
  title: PropTypes.string.isRequired,
  description: PropTypes.string
});

let Steps = ({ classes, children, steps }) => {
  return (
    <div className={classes.root}>
      {steps.map((step, index) => {
        return <StepItem key={step.title} number={index + 1} step={step} />;
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
  }
})(StepItem);

export default Steps;
