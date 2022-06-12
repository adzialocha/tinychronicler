import { createRoot } from 'react-dom/client';

import App from '~/components/App';

const container = document.getElementById('app');

if (!container) {
  throw Error('Something went seriously wrong ..');
}

const version = container.getAttribute('data-version');
const root = createRoot(container);
root.render(<App version={version ? version : ''} />);
