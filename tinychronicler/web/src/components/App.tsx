import { Fragment } from 'react';
import { HashRouter } from 'react-router-dom';
import { createGlobalStyle, ThemeProvider } from 'styled-components';
import { styleReset } from 'react95';

import originalTheme from 'react95/dist/themes/original';
import ms_sans_serif from 'react95/dist/fonts/ms_sans_serif.woff2';
import ms_sans_serif_bold from 'react95/dist/fonts/ms_sans_serif_bold.woff2';

import Header from '~/components/Header';
import Main from '~/components/Main';
import Router from '~/Router';

const GlobalStyle = createGlobalStyle`
  ${styleReset}

  @font-face {
    font-family: 'ms_sans_serif';
    src: url('${ms_sans_serif}') format('woff2');
    font-weight: 400;
    font-style: normal
  }

  @font-face {
    font-family: 'ms_sans_serif';
    src: url('${ms_sans_serif_bold}') format('woff2');
    font-weight: bold;
    font-style: normal
  }

  body {
    font-family: 'ms_sans_serif';
    background-color: rgb(0, 128, 128);
  }

  html,
  body,
  #app {
    height: 100%;
  }

  td {
    word-wrap: anywhere;
  }

  @media (max-width: 900px) {
    td {
      max-width: 100px;
      text-overflow: ellipsis;
      overflow: hidden;
      word-wrap: normal;
      white-space: nowrap;
    }

    td:last-child {
      white-space: normal;
    }
  }
`;

type Props = {
  version: string;
};

const App = ({ version }: Props) => {
  return (
    <Fragment>
      <GlobalStyle />
      <ThemeProvider theme={originalTheme}>
        <HashRouter>
          <Main>
            <Router />
          </Main>
          <Header version={version} />
        </HashRouter>
      </ThemeProvider>
    </Fragment>
  );
};

export default App;
