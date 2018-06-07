import React from "react";

export default class HomepageBenefices extends React.Component {
  render() {
    return (
      <section id="benefices" className="section ">
        <div className="container">
          <div
            className="content"
            dangerouslySetInnerHTML={{
              __html: this.props.data.benefices
            }}
          />
        </div>
      </section>
    );
  }
}
