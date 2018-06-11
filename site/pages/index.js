import Document, { meta } from "../content/index.md";
import Header from "../components/ui/Header";
import ButtonLink from "../components/ui/ButtonLink";
import Section from "../components/ui/Section";
import backgroundImageUrl from "../static/images/header.png";
import Layout from "../components/ui/Layout";
import Container from "../components/ui/Container";
import injectSheet from "react-jss";

const Index = ({ classes }) => {
  return (
    <Layout>
      <Header
        backgroundImageUrl={backgroundImageUrl}
        title={meta.header.title}
        subtitle={meta.header.subtitle}
        callToActionText={meta.header.callToAction.text}
        callToActionLink={meta.header.callToAction.link}
      />
      <Section type="primary">
        <Container>
          <div style={{ fontSize: "25px" }}>{meta.sectionPainPoint.title}</div>
          <div style={{ fontSize: "25px" }}>
            {meta.sectionPainPoint.question}
          </div>
        </Container>
      </Section>
      <Section type="secondary">
        <Container>
          <div style={{ fontSize: "25px" }}>{meta.sectionBenefices.title}</div>
          <ul style={{ fontSize: "25px" }}>
            {meta.sectionBenefices.points.map(point => {
              return <li>{point}</li>;
            })}
          </ul>
        </Container>
      </Section>
    </Layout>
  );
};

export default Index;
