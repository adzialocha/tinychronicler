import { Routes, Route } from 'react-router-dom';

import Chronicles from '~/views/Chronicles';
import ChroniclesEdit from '~/views/ChroniclesEdit';
import ChroniclesNew from '~/views/ChroniclesNew';
import CompositionsShow from '~/views/CompositionsShow';
import Dashboard from '~/views/Dashboard';
import FilesShow from '~/views/FilesShow';
import Settings from '~/views/Settings';

const Router = () => {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/chronicles" element={<Chronicles />} />
      <Route path="/chronicles/new" element={<ChroniclesNew />} />
      <Route path="/chronicles/:id/edit" element={<ChroniclesEdit />} />
      <Route
        path="/chronicles/:chronicleId/files/:id"
        element={<FilesShow />}
      />
      <Route
        path="/chronicles/:chronicleId/compositions/:id"
        element={<CompositionsShow />}
      />
      <Route path="/settings" element={<Settings />} />
    </Routes>
  );
};

export default Router;
