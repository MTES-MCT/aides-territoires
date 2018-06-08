import React from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import moment from "moment";

export default class extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      date: moment()
    };
  }

  handleDisplayedValue = () => {
    const dateAsString = moment(this.props.input.value).format("DD/MM/YYYY");
    return dateAsString;
  };

  // pass date as a Date string to Final Form
  handleInputChange = date => {
    this.setState({
      date
    });
    const dateAsString = date.toString();
    this.props.input.onChange(dateAsString);
  };

  render() {
    const {
      input,
      label,
      meta: { touched, error }
    } = this.props;
    return (
      <div className="field">
        <label className="label">{label}</label>
        <DatePicker
          className="input is-large"
          {...input}
          value={this.handleDisplayedValue()}
          // override final form value and onChange props, because DatePicker
          // is using an object and final form wants a string
          onChange={this.handleInputChange}
        />
        {error && touched && <div className="help is-danger">{error}</div>}
      </div>
    );
  }
}
