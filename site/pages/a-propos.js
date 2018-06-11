import Document, { meta } from "../content/a-propos.md";
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
      />
      <Container>
        <Section>
          <Document />
        </Section>
      </Container>
    </Layout>
  );
};

export default Index;
