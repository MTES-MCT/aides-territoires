import React from "react";

export default class SectionChronophage extends React.Component {
  render() {
    return (
      <section id="chronophage" className="section has-primary-background">
        <div className="container ">
          <div
            dangerouslySetInnerHTML={{
              __html: this.props.data.probleme
            }}
          />
        </div>
      </section>
    );
  }
}
